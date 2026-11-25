"""Casos deterministas sin red ni dependencia del reloj del computador."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from core.modelos import Hallazgo, ReporteRespaldo
from core.validacion import LIMITACION, validar_reporte


REFERENCIA = datetime(2026, 11, 25, 12, tzinfo=timezone.utc)


def reporte_correcto():
    return ReporteRespaldo(
        identificador="REP-001",
        modelo_servicio="Infraestructura como servicio",
        activo="Servidor académico",
        fecha_respaldo=REFERENCIA - timedelta(hours=2),
        estado_respaldo="Exitoso",
        porcentaje_completitud=100,
        fecha_ultima_restauracion=REFERENCIA - timedelta(days=1),
        estado_ultima_restauracion="Exitoso",
        tiempo_restauracion_minutos=20,
        tiempo_maximo_recuperacion_minutos=60,
        antiguedad_maxima_respaldo_horas=24,
        antiguedad_maxima_prueba_restauracion_dias=30,
        observaciones="Evidencia de laboratorio",
    )


class PruebasValidacion(unittest.TestCase):
    def validar(self, **cambios):
        return validar_reporte(replace(reporte_correcto(), **cambios), REFERENCIA)

    def comprobar_hallazgo(self, hallazgos, prioridad, texto):
        self.assertTrue(any(
            hallazgo.prioridad == prioridad
            and texto in (hallazgo.evidencia + hallazgo.interpretacion + hallazgo.recomendacion)
            for hallazgo in hallazgos
        ), hallazgos)
        self.assertFalse(any(h.prioridad == "Baja" for h in hallazgos))

    def test_reporte_correcto(self):
        hallazgos = self.validar()
        self.assertEqual(len(hallazgos), 1)
        self.assertEqual(hallazgos[0].prioridad, "Baja")
        self.assertEqual(hallazgos[0].interpretacion,
                         "No se identificaron incumplimientos objetivos en los datos suministrados.")
        self.assertEqual(hallazgos[0].limitacion, LIMITACION)

    def test_respaldo_fallido(self):
        self.comprobar_hallazgo(self.validar(estado_respaldo="Fallido"),
                               "Alta", "No existe evidencia de una copia satisfactoria")

    def test_respaldo_incompleto_por_estado(self):
        self.comprobar_hallazgo(self.validar(estado_respaldo="Incompleto"), "Alta", "100%")

    def test_respaldo_incompleto_por_porcentaje(self):
        self.comprobar_hallazgo(self.validar(porcentaje_completitud=75), "Alta", "75%")

    def test_respaldo_antiguo_prioridad_media(self):
        self.comprobar_hallazgo(self.validar(fecha_respaldo=REFERENCIA - timedelta(hours=30)),
                               "Media", "30.00 horas")

    def test_respaldo_antiguo_prioridad_alta(self):
        self.comprobar_hallazgo(self.validar(fecha_respaldo=REFERENCIA - timedelta(hours=49)),
                               "Alta", "49.00 horas")

    def test_sin_fecha_restauracion(self):
        hallazgos = self.validar(fecha_ultima_restauracion=None)
        self.comprobar_hallazgo(hallazgos, "Alta", "no demuestra recuperabilidad")
        self.comprobar_hallazgo(hallazgos, "No concluyente", "fecha_ultima_restauracion")

    def test_restauracion_desconocida(self):
        self.comprobar_hallazgo(self.validar(estado_ultima_restauracion="Desconocido"),
                               "Alta", "laboratorio")

    def test_restauracion_fallida(self):
        self.comprobar_hallazgo(self.validar(estado_ultima_restauracion="Fallido"),
                               "Alta", "Investigar el fallo")

    def test_restauracion_antigua(self):
        self.comprobar_hallazgo(
            self.validar(fecha_ultima_restauracion=REFERENCIA - timedelta(days=31)),
            "Media", "31.00 días",
        )

    def test_tiempo_superior_al_permitido(self):
        hallazgos = self.validar(tiempo_restauracion_minutos=90)
        self.comprobar_hallazgo(hallazgos, "Alta", "90 minutos; máximo permitido: 60 minutos")
        self.assertIn("no cumple el objetivo", hallazgos[0].interpretacion)

    def test_reporte_sin_informacion(self):
        hallazgos = validar_reporte(ReporteRespaldo(), REFERENCIA)
        self.comprobar_hallazgo(hallazgos, "No concluyente", "identificador, modelo_servicio, activo")
        for campo in (
            "estado_respaldo", "porcentaje_completitud", "fecha_respaldo",
            "antiguedad_maxima_respaldo_horas", "fecha_ultima_restauracion",
            "estado_ultima_restauracion", "antiguedad_maxima_prueba_restauracion_dias",
            "tiempo_restauracion_minutos", "tiempo_maximo_recuperacion_minutos",
        ):
            self.comprobar_hallazgo(hallazgos, "No concluyente", campo)

    def test_cada_dato_esencial_ausente_impide_resultado_satisfactorio(self):
        for campo in reporte_correcto().__dataclass_fields__:
            if campo == "observaciones":
                continue
            with self.subTest(campo=campo):
                self.comprobar_hallazgo(self.validar(**{campo: None}), "No concluyente", campo)

    def test_limites_exactos_no_se_exceden(self):
        hallazgos = self.validar(
            fecha_respaldo=REFERENCIA - timedelta(hours=24),
            fecha_ultima_restauracion=REFERENCIA - timedelta(days=30),
            tiempo_restauracion_minutos=60,
        )
        self.assertEqual([h.prioridad for h in hallazgos], ["Baja"])

    def test_doble_limite_respaldo_todavia_es_media(self):
        self.comprobar_hallazgo(self.validar(fecha_respaldo=REFERENCIA - timedelta(hours=48)),
                               "Media", "48.00 horas")

    def test_fechas_futuras_no_son_satisfactorias(self):
        for campo in ("fecha_respaldo", "fecha_ultima_restauracion"):
            with self.subTest(campo=campo):
                self.comprobar_hallazgo(
                    self.validar(**{campo: REFERENCIA + timedelta(seconds=1)}),
                    "No concluyente", campo,
                )

    def test_restauracion_incompleta(self):
        self.comprobar_hallazgo(self.validar(estado_ultima_restauracion="Incompleto"),
                               "Alta", "no demuestra una restauración satisfactoria")

    def test_respaldo_desconocido(self):
        self.comprobar_hallazgo(self.validar(estado_respaldo="Desconocido"),
                               "No concluyente", "Falta conocer")

    def test_todas_las_reglas_se_ejecutan(self):
        hallazgos = self.validar(
            estado_respaldo="Fallido", porcentaje_completitud=50,
            fecha_respaldo=REFERENCIA - timedelta(hours=80),
            estado_ultima_restauracion="Fallido",
            fecha_ultima_restauracion=REFERENCIA - timedelta(days=40),
            tiempo_restauracion_minutos=90,
        )
        self.assertEqual(len(hallazgos), 6)
        self.assertTrue(all(h.identificador == "REP-001" and h.limitacion == LIMITACION
                            for h in hallazgos))

    def test_faltante_no_oculta_incompletitud_conocida(self):
        hallazgos = self.validar(estado_respaldo="Incompleto", porcentaje_completitud=None)
        self.comprobar_hallazgo(hallazgos, "Alta", "no suministrado")
        self.comprobar_hallazgo(hallazgos, "No concluyente", "porcentaje_completitud")


class PruebasModelos(unittest.TestCase):
    def test_estados_y_modelo_invalidos(self):
        for campo in ("modelo_servicio", "estado_respaldo", "estado_ultima_restauracion"):
            with self.subTest(campo=campo), self.assertRaises(ValueError):
                replace(reporte_correcto(), **{campo: "No admitido"})

    def test_numeros_invalidos(self):
        campos = (
            "porcentaje_completitud", "tiempo_restauracion_minutos",
            "tiempo_maximo_recuperacion_minutos", "antiguedad_maxima_respaldo_horas",
            "antiguedad_maxima_prueba_restauracion_dias",
        )
        for campo in campos:
            for valor in (-1, float("nan"), float("inf"), True, "10"):
                with self.subTest(campo=campo, valor=valor), self.assertRaises(ValueError):
                    replace(reporte_correcto(), **{campo: valor})
        with self.assertRaises(ValueError):
            replace(reporte_correcto(), porcentaje_completitud=101)

    def test_fechas_de_tipo_invalido(self):
        for campo in ("fecha_respaldo", "fecha_ultima_restauracion"):
            with self.subTest(campo=campo), self.assertRaises(ValueError):
                replace(reporte_correcto(), **{campo: "2026-02-30"})
        with self.assertRaises(ValueError):
            validar_reporte(reporte_correcto(), "2026-11-25")

    def test_zonas_horarias_equivalentes(self):
        zona_colombia = timezone(timedelta(hours=-5))
        reporte = replace(reporte_correcto(),
                          fecha_respaldo=(REFERENCIA - timedelta(hours=2)).astimezone(zona_colombia))
        self.assertEqual(validar_reporte(reporte, REFERENCIA),
                         validar_reporte(reporte_correcto(), REFERENCIA.astimezone(zona_colombia)))

    def test_fechas_sin_zona_se_interpretan_como_utc(self):
        reporte = replace(reporte_correcto(), fecha_respaldo=(REFERENCIA - timedelta(hours=2)).replace(tzinfo=None))
        self.assertEqual(validar_reporte(reporte, REFERENCIA.replace(tzinfo=None)),
                         validar_reporte(reporte_correcto(), REFERENCIA))

    def test_prioridad_invalida(self):
        with self.assertRaises(ValueError):
            Hallazgo("REP-001", "evidencia", "interpretación", "Crítica", "recomendación", "limitación")

    def test_textos_vacios_son_datos_ausentes(self):
        reporte = replace(reporte_correcto(), identificador="  ", activo="")
        self.assertIsNone(reporte.identificador)
        self.assertIsNone(reporte.activo)
        self.assertTrue(any(h.prioridad == "No concluyente"
                            for h in validar_reporte(reporte, REFERENCIA)))

    def test_ceros_son_valores_conocidos(self):
        reporte = replace(reporte_correcto(), fecha_respaldo=REFERENCIA,
                          fecha_ultima_restauracion=REFERENCIA,
                          antiguedad_maxima_respaldo_horas=0,
                          antiguedad_maxima_prueba_restauracion_dias=0,
                          tiempo_restauracion_minutos=0, tiempo_maximo_recuperacion_minutos=0)
        self.assertEqual(validar_reporte(reporte, REFERENCIA)[0].prioridad, "Baja")


if __name__ == "__main__":
    unittest.main()
