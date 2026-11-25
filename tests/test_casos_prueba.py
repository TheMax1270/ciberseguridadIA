"""Verificar el conjunto académico con expectativas independientes del motor."""

from collections import Counter
from dataclasses import fields
from datetime import datetime
import json
from pathlib import Path
import unittest

from core.modelos import MODELOS_SERVICIO, PRIORIDADES, ReporteRespaldo
from core.validacion import LIMITACION, validar_reporte


RUTA_CASOS = Path(__file__).resolve().parents[1] / "data" / "casos_prueba.json"
FECHA_REFERENCIA = datetime.fromisoformat("2026-11-25T12:00:00")


def convertir_entrada(entrada):
    """Convertir solo fechas ISO explícitas, preservando los datos ausentes."""
    datos = dict(entrada)
    for campo in ("fecha_respaldo", "fecha_ultima_restauracion"):
        if datos[campo] is not None:
            datos[campo] = datetime.fromisoformat(datos[campo])
    return ReporteRespaldo(**datos)


class PruebasCasosAcademicos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documento = json.loads(RUTA_CASOS.read_text(encoding="utf-8"))
        cls.casos = cls.documento["casos"]

    def test_total_y_referencia_fija(self):
        self.assertEqual(len(self.casos), 20)
        self.assertEqual(self.documento["fecha_referencia"], "2026-11-25T12:00:00")

    def test_distribucion_por_categoria(self):
        self.assertEqual(Counter(caso["categoria"] for caso in self.casos),
                         {"Problematico": 8, "Legitimo": 8, "Ambiguo": 4})

    def test_reservados_para_evaluacion_final(self):
        for caso in self.casos:
            self.assertIs(type(caso["reservado_evaluacion_final"]), bool)
        reservados = [caso for caso in self.casos if caso["reservado_evaluacion_final"]]
        self.assertEqual(len(reservados), 10)
        self.assertEqual(Counter(caso["categoria"] for caso in reservados),
                         {"Problematico": 4, "Legitimo": 4, "Ambiguo": 2})
        self.assertEqual({caso["identificador"] for caso in reservados},
                         {"P05", "P06", "P07", "P08", "L05", "L06", "L07", "L08", "A03", "A04"})

    def test_identificadores_unicos_y_coherentes(self):
        identificadores = [caso["identificador"] for caso in self.casos]
        self.assertEqual(len(set(identificadores)), 20)
        esperados = ({f"P{i:02d}" for i in range(1, 9)}
                     | {f"L{i:02d}" for i in range(1, 9)}
                     | {f"A{i:02d}" for i in range(1, 5)})
        self.assertEqual(set(identificadores), esperados)
        for caso in self.casos:
            self.assertEqual(caso["identificador"], caso["entrada"]["identificador"])

    def test_estructura_completa_y_expectativas_explicitas(self):
        campos_caso = {"identificador", "categoria", "descripcion", "entrada",
                       "resultado_esperado", "justificacion", "reservado_evaluacion_final"}
        campos_entrada = {campo.name for campo in fields(ReporteRespaldo)}
        for caso in self.casos:
            with self.subTest(caso=caso["identificador"]):
                self.assertEqual(set(caso), campos_caso)
                self.assertEqual(set(caso["entrada"]), campos_entrada)
                for campo in ("descripcion", "justificacion"):
                    self.assertIsInstance(caso[campo], str)
                    self.assertTrue(caso[campo].strip())
                self.assertEqual(set(caso["resultado_esperado"]), {"hallazgos"})
                self.assertTrue(caso["resultado_esperado"]["hallazgos"])
                for esperado in caso["resultado_esperado"]["hallazgos"]:
                    self.assertEqual(set(esperado), {"prioridad", "evidencia_contiene",
                                                    "interpretacion_contiene"})
                    self.assertIn(esperado["prioridad"], PRIORIDADES)
                    for campo in ("evidencia_contiene", "interpretacion_contiene"):
                        self.assertIsInstance(esperado[campo], str)
                        self.assertTrue(esperado[campo].strip())

    def test_tres_modelos_de_servicio_por_categoria(self):
        for categoria in ("Problematico", "Legitimo", "Ambiguo"):
            modelos = {caso["entrada"]["modelo_servicio"] for caso in self.casos
                       if caso["categoria"] == categoria}
            self.assertEqual(modelos, set(MODELOS_SERVICIO))

    def test_todas_las_entradas_se_convierten_al_modelo(self):
        for caso in self.casos:
            with self.subTest(caso=caso["identificador"]):
                reporte = convertir_entrada(caso["entrada"])
                self.assertIsInstance(reporte, ReporteRespaldo)
                self.assertEqual(reporte.identificador, caso["identificador"])

    def test_resultados_esperados_de_los_20_casos(self):
        # Se incluyen los reservados para comprobar coherencia, sin ajustar reglas.
        for caso in self.casos:
            with self.subTest(caso=caso["identificador"]):
                reporte = convertir_entrada(caso["entrada"])
                obtenidos = validar_reporte(reporte, FECHA_REFERENCIA)
                esperados = caso["resultado_esperado"]["hallazgos"]
                self.assertEqual(len(obtenidos), len(esperados))
                pendientes = list(obtenidos)
                for esperado in esperados:
                    coincidencias = [h for h in pendientes
                                     if h.prioridad == esperado["prioridad"]
                                     and esperado["evidencia_contiene"] in h.evidencia
                                     and esperado["interpretacion_contiene"] in h.interpretacion]
                    self.assertTrue(coincidencias, (caso["identificador"], esperado, pendientes))
                    pendientes.remove(coincidencias[0])
                self.assertFalse(pendientes)
                for hallazgo in obtenidos:
                    self.assertEqual(hallazgo.identificador, caso["identificador"])
                    self.assertTrue(hallazgo.recomendacion.strip())
                    self.assertEqual(hallazgo.limitacion, LIMITACION)
                prioridades = {hallazgo.prioridad for hallazgo in obtenidos}
                if caso["categoria"] == "Legitimo":
                    self.assertFalse(prioridades & {"Alta", "Media"})
                    self.assertEqual(prioridades, {"Baja"})
                elif caso["categoria"] == "Ambiguo":
                    self.assertIn("No concluyente", prioridades)
                    self.assertNotIn("Baja", prioridades)
                else:
                    self.assertTrue(prioridades & {"Alta", "Media"})


if __name__ == "__main__":
    unittest.main()
