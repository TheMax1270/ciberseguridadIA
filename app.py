"""Interfaz académica; no ejecuta cambios sobre infraestructura."""

from collections import Counter
from datetime import datetime, time, timezone
import json
from uuid import uuid4

import streamlit as st

from core.carga import cargar_casos, convertir_entrada
from core.analisis_ia import MODELO, MENSAJE_NO_DISPONIBLE, analizar_con_ia, comprobar_ollama
from core.comparacion import comparar_analisis
from core.exportacion import exportar_analisis
from core.modelos import ESTADOS, MODELOS_SERVICIO
from core.validacion import validar_reporte


ETIQUETAS = {
    "identificador": "Identificador", "modelo_servicio": "Modelo de servicio",
    "activo": "Activo", "fecha_respaldo": "Fecha del respaldo",
    "estado_respaldo": "Estado del respaldo", "porcentaje_completitud": "Completitud (%)",
    "fecha_ultima_restauracion": "Fecha de la última restauración",
    "estado_ultima_restauracion": "Estado de la última restauración",
    "tiempo_restauracion_minutos": "Tiempo de restauración (minutos)",
    "tiempo_maximo_recuperacion_minutos": "Tiempo máximo de recuperación (minutos)",
    "antiguedad_maxima_respaldo_horas": "Antigüedad máxima del respaldo (horas)",
    "antiguedad_maxima_prueba_restauracion_dias": "Antigüedad máxima de la prueba (días)",
    "observaciones": "Observaciones",
}


def fecha_opcional(campo):
    st.caption(ETIQUETAS[campo] + " (UTC; fecha y hora vacías = sin información)")
    izquierda, derecha = st.columns(2)
    fecha = izquierda.date_input("Fecha", value=None, key=campo + "_fecha")
    hora = derecha.time_input("Hora UTC", value=None, key=campo + "_hora")
    if (fecha is None) != (hora is None):
        st.warning("Complete fecha y hora, o deje ambas vacías. La fecha parcial no se analizará.")
    return datetime.combine(fecha, hora) if fecha is not None and hora is not None else None


def formulario_manual():
    st.subheader("Ingreso manual")
    st.caption("Deje vacíos los datos desconocidos. Para registrar una fecha, indique también su hora.")
    with st.form("reporte_manual"):
        entrada = {}
        for campo in ("identificador", "activo"):
            entrada[campo] = st.text_input(ETIQUETAS[campo]).strip() or None
        entrada["modelo_servicio"] = st.selectbox(
            "Modelo de servicio", [None, *MODELOS_SERVICIO],
            format_func=lambda valor: valor or "Sin información")
        entrada["fecha_respaldo"] = fecha_opcional("fecha_respaldo")
        entrada["estado_respaldo"] = st.selectbox(
            "Estado del respaldo", [None, *ESTADOS], format_func=lambda valor: valor or "Sin información")
        entrada["porcentaje_completitud"] = st.number_input(
            ETIQUETAS["porcentaje_completitud"], min_value=0.0, max_value=100.0, value=None)
        entrada["fecha_ultima_restauracion"] = fecha_opcional("fecha_ultima_restauracion")
        entrada["estado_ultima_restauracion"] = st.selectbox(
            "Estado de la última restauración", [None, *ESTADOS],
            format_func=lambda valor: valor or "Sin información")
        for campo in ("tiempo_restauracion_minutos", "tiempo_maximo_recuperacion_minutos",
                      "antiguedad_maxima_respaldo_horas", "antiguedad_maxima_prueba_restauracion_dias"):
            entrada[campo] = st.number_input(ETIQUETAS[campo], min_value=0.0, value=None)
        entrada["observaciones"] = st.text_area("Observaciones").strip() or None
        if st.form_submit_button("Actualizar evidencia"):
            st.session_state["entrada_manual"] = entrada
    st.caption("Pulse Actualizar evidencia para revisar los datos antes de analizarlos.")
    return st.session_state.get("entrada_manual")


def seleccionar_caso():
    casos = cargar_casos()
    categoria = st.selectbox("Categoría", ["Todos", "Problematico", "Legitimo", "Ambiguo"])
    disponibles = [c for c in casos if categoria == "Todos" or c["categoria"] == categoria]
    if not disponibles:
        st.warning("No hay casos para la categoría seleccionada.")
        return None
    caso = st.selectbox("Caso de laboratorio", disponibles,
                        format_func=lambda c: f"{c['identificador']} — {c['descripcion']}")
    for etiqueta, valor in (("Identificador", caso["identificador"]),
                            ("Categoría", caso["categoria"]),
                            ("Modelo de servicio", caso["entrada"]["modelo_servicio"]),
                            ("Activo", caso["entrada"]["activo"])):
        st.write(f"**{etiqueta}:** {valor}")
    st.write(caso["descripcion"])
    if caso["reservado_evaluacion_final"]:
        st.warning("Caso reservado para evaluación final")
    else:
        st.caption("Reservado para evaluación final: No")
    return caso["entrada"]


def mostrar_evidencia(entrada):
    st.subheader("Evidencia recibida")
    filas = []
    for campo, etiqueta in ETIQUETAS.items():
        valor = entrada.get(campo)
        if isinstance(valor, datetime):
            valor = valor.isoformat(sep=" ")
        filas.append({"Campo": etiqueta, "Valor": "Sin información" if valor is None else str(valor)})
    st.table(filas)


def mostrar_resultados(resultado):
    st.subheader("Resultados de la validación objetiva")
    st.write(f"**Identificador de análisis:** {resultado['identificador']}")
    st.caption(f"Fecha de análisis: {resultado['fecha'].isoformat()} · "
               f"Referencia UTC: {resultado['referencia'].isoformat()}")
    hallazgos = resultado["hallazgos"]
    cantidades = Counter(h.prioridad for h in hallazgos)
    columnas = st.columns(5)
    columnas[0].metric("Total de hallazgos", len(hallazgos))
    for columna, prioridad in zip(columnas[1:], ("Alta", "Media", "Baja", "No concluyente")):
        columna.metric(prioridad, cantidades[prioridad])
    for numero, hallazgo in enumerate(hallazgos, 1):
        with st.expander(f"Hallazgo {numero} · {hallazgo.prioridad}", expanded=True):
            indicador = {"Alta": st.error, "Media": st.warning,
                         "Baja": st.success, "No concluyente": st.info}[hallazgo.prioridad]
            st.write("**Identificador:**", hallazgo.identificador)
            indicador(f"Prioridad: {hallazgo.prioridad}")
            for campo, etiqueta in (("evidencia", "Evidencia"), ("interpretacion", "Interpretación"),
                                    ("recomendacion", "Recomendación"), ("limitacion", "Limitación")):
                st.write(f"**{etiqueta}:**")
                st.text(getattr(hallazgo, campo))
    st.subheader("Revisión humana requerida")
    st.info("Los hallazgos representan apoyo para la toma de decisiones. Una persona debe "
            "revisar la evidencia antes de aprobar cambios, ejecutar restauraciones o "
            "declarar que un servicio es recuperable.")


def mostrar_capa_ia(resultado):
    st.caption("Apoyo interpretativo local; no sustituye las reglas ni ejecuta acciones.")
    st.write(f"**Modelo utilizado:** {MODELO}")
    st.caption("Conexión exclusiva a 127.0.0.1:11434. No se envían identificadores, nombres "
               "de activos ni observaciones al modelo. Use solamente datos sintéticos.")
    if st.button("Comprobar Ollama local", key="comprobar_ollama"):
        st.session_state["estado_ollama"] = comprobar_ollama()
    estado = st.session_state.get("estado_ollama")
    if estado:
        st.write("**Estado de Ollama:**", estado["mensaje"])
        if not estado["servicio_disponible"] or not estado["modelo_instalado"]:
            st.warning(MENSAJE_NO_DISPONIBLE)
    else:
        st.write("**Estado de Ollama:** sin comprobar; se verificará antes del análisis asistido.")
    st.info("Revisión humana requerida. Una persona debe contrastar la interpretación con "
            "las evidencias antes de aprobar cambios o declarar recuperabilidad.")
    if resultado is None:
        st.button("Ejecutar análisis asistido", disabled=True, key="ejecutar_ia")
        st.caption("Primero ejecute la validación mediante reglas para la evidencia seleccionada.")
        return
    if st.button("Ejecutar análisis asistido", key="ejecutar_ia"):
        with st.spinner("Consultando el modelo local; espera de generación limitada a 45 segundos por operación…"):
            asistido = analizar_con_ia(resultado["reporte"], resultado["hallazgos"])
        asistido["identificador_validacion"] = resultado["identificador"]
        resultado["analisis_ia"] = asistido
        resultado["comparacion"] = comparar_analisis(resultado["hallazgos"], asistido)
        # Refrescar la exportación de la misma ejecución objetiva, sin guardar en disco.
        resultado["json"] = exportar_analisis(
            resultado["reporte"], resultado["hallazgos"], resultado["identificador"],
            resultado["fecha"], resultado["referencia"], asistido, resultado["comparacion"])
        st.session_state["estado_ollama"] = asistido["estado_ollama"]
        st.rerun()
    if "analisis_ia" in resultado:
        asistido = resultado["analisis_ia"]
        st.write(f"**Identificador del análisis asistido:** {asistido['identificador_analisis']}")
        st.caption(f"Fecha UTC: {asistido['fecha_analisis']} · Modelo: {asistido['modelo']} · "
                   f"Duración: {asistido['duracion_segundos']:.3f} segundos")
        st.write("**Estado de la ejecución:**", asistido["estado"])
        if asistido["estado"] == "no_disponible":
            st.warning(MENSAJE_NO_DISPONIBLE)
        for error in asistido["errores"]:
            st.warning(error)
        for campo, etiqueta in (
            ("interpretacion_general", "Interpretación general"),
            ("nivel_riesgo_sugerido", "Nivel de riesgo sugerido"),
            ("recomendacion", "Recomendación"), ("informacion_faltante", "Información faltante"),
            ("limitacion", "Limitación"), ("decision_humana_requerida", "Decisión humana requerida"),
        ):
            st.write(f"**{etiqueta}:**")
            valor = asistido["respuesta_estructurada"][campo]
            if campo == "decision_humana_requerida":
                st.text("Sí")
            elif isinstance(valor, list):
                st.text("\n".join(valor) if valor else "El modelo no señaló información adicional.")
            else:
                st.text(valor)
        st.caption("La salida generada puede contener errores semánticos. Contraste siempre "
                   "las afirmaciones con las reglas; la coincidencia de niveles no certifica el texto.")


def mostrar_comparacion(comparacion):
    st.subheader("Comparación de resultados")
    reglas, asistido = st.columns(2)
    with reglas:
        st.markdown("**Validación mediante reglas**")
        datos = comparacion["validacion_mediante_reglas"]
        st.write("Cantidad de hallazgos:", datos["cantidad_hallazgos"])
        st.write("Prioridad máxima:", datos["prioridad_maxima"])
        st.write("Principales evidencias:")
        for evidencia in datos["principales_evidencias"]:
            st.text(evidencia)
    with asistido:
        st.markdown("**Análisis asistido por inteligencia artificial**")
        for campo, etiqueta in (("nivel_riesgo_sugerido", "Nivel de riesgo sugerido"),
                                ("interpretacion", "Interpretación"),
                                ("recomendacion", "Recomendación"), ("limitacion", "Limitación")):
            st.write(f"**{etiqueta}:**")
            st.text(comparacion["analisis_asistido"][campo])
    st.markdown("**Revisión humana**")
    st.info(comparacion["revision_humana"])


def main():
    st.set_page_config(page_title="Validación de respaldos", page_icon="☁️", layout="wide")
    st.title("Asistente de validación de respaldos")
    st.write("Prototipo académico para analizar evidencia de copias de respaldo y pruebas "
             "de restauración en servicios de nube.")
    st.markdown("**Evidencia → Validación objetiva → Análisis → Revisión humana**")
    st.info("El sistema no declara que un servicio sea recuperable únicamente porque exista "
            "una copia de respaldo.")
    with st.sidebar:
        st.header("Fuente de datos")
        fuente = st.radio("Seleccionar fuente", ["Casos de laboratorio", "Ingreso manual"])
        st.header("Fecha de referencia")
        st.caption("Todas las fechas se interpretan en UTC.")
        fecha = st.date_input("Fecha de referencia", value=datetime(2026, 11, 25).date())
        hora = st.time_input("Hora de referencia", value=time(12), step=60)
    reglas, ia = st.tabs(["Validación mediante reglas", "Análisis asistido por inteligencia artificial"])
    with reglas:
        try:
            entrada = seleccionar_caso() if fuente == "Casos de laboratorio" else formulario_manual()
            if fecha is None or hora is None:
                st.warning("Indique fecha y hora de referencia antes de analizar.")
                with ia:
                    mostrar_capa_ia(None)
                return
            referencia = datetime.combine(fecha, hora, tzinfo=timezone.utc)
            if entrada is None:
                st.session_state.pop("resultado", None)
                with ia:
                    mostrar_capa_ia(None)
                return
            mostrar_evidencia(entrada)
            firma = json.dumps([fuente, entrada, referencia.isoformat()], default=str, sort_keys=True)
            if st.session_state.get("firma") != firma:
                st.session_state.pop("resultado", None)
                st.session_state["firma"] = firma
            if st.button("Analizar respaldo", type="primary"):
                reporte = convertir_entrada(entrada)
                hallazgos = validar_reporte(reporte, referencia)
                identificador = str(uuid4())
                fecha_analisis = datetime.now(timezone.utc)
                st.session_state["resultado"] = {
                    "identificador": identificador, "fecha": fecha_analisis,
                    "referencia": referencia, "hallazgos": hallazgos, "reporte": reporte,
                    "json": exportar_analisis(reporte, hallazgos, identificador,
                                              fecha_analisis, referencia),
                }
            if "resultado" in st.session_state:
                mostrar_resultados(st.session_state["resultado"])
        except (ValueError, TypeError, KeyError, OSError) as error:
            st.session_state.pop("resultado", None)
            st.error(f"No fue posible procesar la entrada: {error}")
    resultado = st.session_state.get("resultado")
    with ia:
        mostrar_capa_ia(resultado)
    if resultado:
        if "comparacion" in resultado:
            mostrar_comparacion(resultado["comparacion"])
        st.download_button("Descargar resultado JSON", data=resultado["json"],
                           file_name=f"analisis_{resultado['identificador']}.json", mime="application/json")


if __name__ == "__main__":
    main()
