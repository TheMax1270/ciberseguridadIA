"""Pruebas de la entrada usada por la interfaz y de su exportación."""

from dataclasses import asdict
from datetime import datetime
import json
import unittest

from core.carga import cargar_casos, convertir_entrada
from core.exportacion import exportar_analisis
from core.validacion import validar_reporte


REFERENCIA = datetime(2026, 11, 25, 12)


class PruebasCargaExportacion(unittest.TestCase):
    def setUp(self):
        self.casos = cargar_casos()
        self.reporte = convertir_entrada(next(c["entrada"] for c in self.casos
                                              if c["identificador"] == "P08"))
        self.hallazgos = validar_reporte(self.reporte, REFERENCIA)
        self.texto = exportar_analisis(self.reporte, self.hallazgos, "analisis-prueba",
                                      REFERENCIA, REFERENCIA)
        self.resultado = json.loads(self.texto)

    def test_carga_20_casos(self):
        self.assertEqual(len(self.casos), 20)

    def test_conversion_sin_mutar_json(self):
        entrada = self.casos[0]["entrada"]
        original = dict(entrada)
        reporte = convertir_entrada(entrada)
        self.assertIsInstance(reporte.fecha_respaldo, datetime)
        self.assertEqual(entrada, original)

    def test_exportacion_json_y_trazabilidad(self):
        self.assertEqual(self.resultado["identificador_analisis"], "analisis-prueba")
        self.assertEqual(self.resultado["fecha_analisis"], "2026-11-25T12:00:00+00:00")
        self.assertEqual(self.resultado["fecha_referencia"], "2026-11-25T12:00:00+00:00")
        self.assertEqual(self.resultado["datos_entrada"]["identificador"], "P08")
        self.assertEqual(self.resultado["datos_entrada"]["fecha_respaldo"],
                         self.reporte.fecha_respaldo.isoformat())
        self.assertEqual(set(self.resultado["datos_entrada"]), set(asdict(self.reporte)))

    def test_conservacion_integra_de_hallazgos(self):
        self.assertEqual(self.resultado["hallazgos"], [asdict(h) for h in self.hallazgos])
        self.assertEqual(len(self.resultado["hallazgos"]), 4)

    def test_conteos_por_prioridad(self):
        self.assertEqual(self.resultado["cantidad_por_prioridad"],
                         {"Alta": 4, "Media": 0, "Baja": 0, "No concluyente": 0})
        self.assertEqual(self.resultado["total_hallazgos"], 4)

    def test_revision_humana_y_tipo(self):
        self.assertIs(self.resultado["requiere_revision_humana"], True)
        self.assertEqual(self.resultado["tipo_analisis"], "Validación determinista")

    def test_campos_opcionales_se_conservan_nulos(self):
        entrada = next(c["entrada"] for c in self.casos if c["identificador"] == "P04")
        reporte = convertir_entrada(entrada)
        self.assertIsNone(reporte.fecha_ultima_restauracion)
        hallazgos = validar_reporte(reporte, REFERENCIA)
        resultado = json.loads(exportar_analisis(reporte, hallazgos, "opcional", REFERENCIA, REFERENCIA))
        self.assertIsNone(resultado["datos_entrada"]["fecha_ultima_restauracion"])
        self.assertIsNone(resultado["datos_entrada"]["tiempo_restauracion_minutos"])
        self.assertTrue(any(h["prioridad"] == "No concluyente" for h in resultado["hallazgos"]))

    def test_fecha_invalida_no_se_inventa(self):
        entrada = dict(self.casos[0]["entrada"], fecha_respaldo="2026-02-30T12:00:00")
        with self.assertRaises(ValueError):
            convertir_entrada(entrada)
