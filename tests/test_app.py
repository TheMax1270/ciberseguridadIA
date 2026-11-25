"""Pruebas breves del flujo de sesión, sin automatización visual compleja."""

from datetime import time
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from core.analisis_ia import ErrorIA, MENSAJE_NO_DISPONIBLE
from tests.test_analisis_ia import RESPUESTA, TAGS, salida

RUTA_APP = str(Path(__file__).resolve().parents[1] / "app.py")


class PruebasInterfaz(unittest.TestCase):
    def test_analisis_y_cambio_de_referencia(self):
        app = AppTest.from_file(RUTA_APP, default_timeout=30).run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        resultado = app.session_state["resultado"]
        self.assertEqual(resultado["hallazgos"][0].prioridad, "Alta")
        identificador = resultado["identificador"]
        app.button[0].click().run()
        self.assertNotEqual(app.session_state["resultado"]["identificador"], identificador)
        app.sidebar.time_input[0].set_value(time(13)).run()
        self.assertNotIn("resultado", app.session_state)
        app.button[0].click().run()
        self.assertEqual(app.session_state["resultado"]["referencia"].hour, 13)

    def test_manual_con_datos_desconocidos(self):
        app = AppTest.from_file(RUTA_APP, default_timeout=30).run()
        app.sidebar.radio[0].set_value("Ingreso manual").run()
        app.button[0].click().run()
        self.assertIsNone(app.session_state["entrada_manual"]["fecha_ultima_restauracion"])
        self.assertIsNone(app.session_state["entrada_manual"]["tiempo_restauracion_minutos"])
        app.button[1].click().run()
        self.assertFalse(app.exception)
        hallazgos = app.session_state["resultado"]["hallazgos"]
        self.assertTrue(any(h.prioridad == "No concluyente" for h in hallazgos))

    def test_error_de_entrada_controlado(self):
        app = AppTest.from_file(RUTA_APP, default_timeout=30).run()
        app.sidebar.radio[0].set_value("Ingreso manual").run()
        app.session_state["entrada_manual"] = {"fecha_respaldo": "fecha inválida"}
        app.run()
        app.button[1].click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("No fue posible procesar la entrada" in e.value for e in app.error))

    def test_ollama_ausente_no_afecta_validacion(self):
        with patch("core.analisis_ia.solicitar_json", side_effect=ErrorIA("Servicio no disponible")):
            app = AppTest.from_file(RUTA_APP, default_timeout=30).run()
            app.button[0].click().run()
            originales = list(app.session_state["resultado"]["hallazgos"])
            app.button(key="ejecutar_ia").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any(w.value == MENSAJE_NO_DISPONIBLE for w in app.warning))
            self.assertEqual(app.session_state["resultado"]["hallazgos"], originales)
            self.assertEqual(app.session_state["resultado"]["analisis_ia"]["estado"], "no_disponible")

    def test_ia_se_ejecuta_solo_por_boton_y_se_descarta_al_reanalizar(self):
        respuesta = dict(RESPUESTA, nivel_riesgo_sugerido="Alta",
                         interpretacion_general="El fallo exige investigar la causa.")
        with patch("core.analisis_ia.solicitar_json", side_effect=[TAGS, salida(respuesta)]) as cliente:
            app = AppTest.from_file(RUTA_APP, default_timeout=30).run()
            app.button[0].click().run()
            cliente.assert_not_called()
            app.button(key="ejecutar_ia").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(cliente.call_count, 2)
            self.assertIn("comparacion", app.session_state["resultado"])
            app.button[0].click().run()
            self.assertNotIn("analisis_ia", app.session_state["resultado"])


if __name__ == "__main__":
    unittest.main()
