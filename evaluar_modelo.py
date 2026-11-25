"""Evaluación secuencial real del laboratorio, sin modificar sus reglas ni datos.

Ejecutar con .venv/Scripts/python.exe evaluar_modelo.py. No contiene dobles de IA.
Las métricas describen el sistema con sus controles actuales, no un modelo aislado.
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import re
from statistics import mean
from time import perf_counter
from types import SimpleNamespace
from uuid import uuid4

from core.analisis_ia import MODELO, analizar_con_ia, comprobar_ollama, prioridad_maxima
from core.carga import RUTA_CASOS, cargar_casos, convertir_entrada
from core.comparacion import comparar_analisis
from core.exportacion import exportar_analisis
from core.validacion import validar_reporte


RAIZ = Path(__file__).resolve().parent
REFERENCIA = datetime(2026, 11, 25, 12, tzinfo=timezone.utc)
SERVICIOS = {
    "Infraestructura como servicio": "IaaS",
    "Plataforma como servicio": "PaaS",
    "Software como servicio": "SaaS",
}
ARCHIVOS_PROTEGIDOS = [RUTA_CASOS, RAIZ / "app.py", *sorted((RAIZ / "core").glob("*.py"))]


def huella(archivo):
    return hashlib.sha256(archivo.read_bytes()).hexdigest()


def comprobar_laboratorio(casos):
    """Verificar identidad y distribución del conjunto antes de ejecutar el modelo."""
    if len(casos) != 20 or Counter(c["categoria"] for c in casos) != {
            "Problematico": 8, "Legitimo": 8, "Ambiguo": 4}:
        raise ValueError("El laboratorio debe contener exactamente 8/8/4 casos.")
    identificadores = [c["identificador"] for c in casos]
    if len(set(identificadores)) != 20:
        raise ValueError("Los identificadores del laboratorio no son únicos.")
    for caso in casos:
        if (not re.fullmatch(r"[PLA]\d{2}", caso["identificador"])
                or caso["entrada"]["identificador"] != caso["identificador"]):
            raise ValueError("Identificador del laboratorio inválido o incoherente.")
    documento = json.loads(RUTA_CASOS.read_text(encoding="utf-8"))
    if documento["fecha_referencia"] != "2026-11-25T12:00:00":
        raise ValueError("La fecha original no coincide con la referencia del laboratorio.")


def contrastar_expectativa(hallazgos, esperado):
    """Cotejar TODOS los hallazgos con las expectativas existentes, sin recalcular reglas."""
    pendientes = list(hallazgos)
    faltantes = []
    for expectativa in esperado["hallazgos"]:
        coincidencia = next((h for h in pendientes
                            if h.prioridad == expectativa["prioridad"]
                            and expectativa["evidencia_contiene"] in h.evidencia
                            and expectativa["interpretacion_contiene"] in h.interpretacion), None)
        if coincidencia is None:
            faltantes.append(expectativa)
        else:
            pendientes.remove(coincidencia)
    return {"coincide": not faltantes and not pendientes,
            "expectativas_no_encontradas": faltantes,
            "hallazgos_adicionales": [h.evidencia for h in pendientes]}


def detectar_incidencias(hallazgos, asistido, contraste, comparacion):
    """Señales mecánicas: ninguna de ellas sustituye una revisión de significado."""
    incidencias = []
    firmas = [(h.evidencia, h.interpretacion, h.prioridad, h.recomendacion, h.limitacion)
              for h in hallazgos]
    if any(n > 1 for n in Counter(firmas).values()):
        incidencias.append("Hallazgos deterministas exactamente duplicados.")
    campos_ausentes = Counter()
    for hallazgo in hallazgos:
        if hallazgo.prioridad == "No concluyente" and ": faltan " in hallazgo.evidencia:
            texto = hallazgo.evidencia.split(": faltan ", 1)[1].rstrip(".")
            campos_ausentes.update(c.strip() for c in texto.split(","))
    for campo, cantidad in campos_ausentes.items():
        if cantidad > 1:
            incidencias.append(f"Posible solapamiento: {campo} figura como ausente en {cantidad} reglas; puede ser legítimo.")
    if not contraste["coincide"]:
        incidencias.append("Los hallazgos deterministas difieren de la expectativa del laboratorio.")
    if asistido["estado"] != "completado":
        incidencias.append("IA sin respuesta validada: no atribuir su resultado de reserva al modelo.")
    elif comparacion["coinciden_niveles"] is False:
        incidencias.append("Discrepancia entre prioridad de reglas y nivel sugerido por IA.")
    faltantes = asistido["respuesta_estructurada"]["informacion_faltante"]
    if len(faltantes) != len(set(f.strip().casefold() for f in faltantes)):
        incidencias.append("La lista de información faltante contiene textos repetidos.")
    if asistido["estado"] == "completado":
        entrada = asistido["entrada_utilizada"]
        for campo in dict.fromkeys(f.strip() for f in faltantes):
            if campo in entrada and entrada[campo] is not None and entrada[campo] != "Desconocido":
                incidencias.append(
                    f"Posible inconsistencia: la IA enumera como faltante el campo {campo}, "
                    "pero tiene un valor suministrado. Revisar si solicita evidencia adicional.")
    return incidencias


def evaluar_caso(caso, ejecucion):
    inicio = perf_counter()
    identificador = str(uuid4())
    fecha = datetime.now(timezone.utc)
    esperado = caso["resultado_esperado"]
    prioridad_esperada = prioridad_maxima([
        SimpleNamespace(prioridad=e["prioridad"]) for e in esperado["hallazgos"]])
    ficha = {
        "identificador": caso["identificador"], "categoria": caso["categoria"],
        "modelo_servicio": SERVICIOS[caso["entrada"]["modelo_servicio"]],
        "reservado_evaluacion_final": caso["reservado_evaluacion_final"],
        "resultado_esperado": esperado, "prioridad_maxima_esperada": prioridad_esperada,
        "cantidad_hallazgos_deterministas": None, "prioridad_maxima_reglas": None,
        "evidencias_deterministas": None, "recomendaciones_reglas": None,
        "reglas_ejecutadas": False, "reglas_coinciden_con_esperado": None,
        "respuesta_ia_valida": False, "estado_ia": "no_ejecutado",
        "nivel_riesgo_sugerido_ia": None, "coinciden_reglas_ia": None,
        "ia_coincide_con_nivel_esperado": None,
        "interpretacion_ia": None, "recomendacion_ia": None,
        "informacion_faltante_ia": None, "limitacion_ia": None,
        "tiempo_respuesta_segundos": None, "duracion_total_caso_segundos": None,
        "errores": [], "incidencias_automaticas": [],
        "revision_semantica_humana": "Pendiente", "requiere_revision_humana": True,
    }
    documento = {
        "identificador_analisis": identificador, "fecha_analisis": fecha.isoformat(),
        "fecha_referencia": REFERENCIA.isoformat(), "modelo": MODELO,
        "ejecucion_evaluacion": ejecucion,
    }
    try:
        reporte = convertir_entrada(caso["entrada"])
        hallazgos = validar_reporte(reporte, REFERENCIA)
        ficha.update(reglas_ejecutadas=True, cantidad_hallazgos_deterministas=len(hallazgos),
                     prioridad_maxima_reglas=prioridad_maxima(hallazgos),
                     evidencias_deterministas=[h.evidencia for h in hallazgos],
                     recomendaciones_reglas=[h.recomendacion for h in hallazgos])
        contraste = contrastar_expectativa(hallazgos, esperado)
        ficha["reglas_coinciden_con_esperado"] = contraste["coincide"]
        documento["contraste_expectativa_determinista"] = contraste
        # La llamada es real y síncrona. El propio módulo comprueba modelo y servicio.
        asistido = analizar_con_ia(reporte, hallazgos)
        asistido["identificador_validacion"] = identificador
        comparacion = comparar_analisis(hallazgos, asistido)
        respuesta = asistido["respuesta_estructurada"]
        valida = asistido["estado"] == "completado"
        ficha.update(respuesta_ia_valida=valida, estado_ia=asistido["estado"],
                     tiempo_respuesta_segundos=asistido["duracion_segundos"],
                     coinciden_reglas_ia=comparacion["coinciden_niveles"])
        ficha["errores"].extend(asistido["errores"])
        if valida:
            ficha.update(nivel_riesgo_sugerido_ia=respuesta["nivel_riesgo_sugerido"],
                         interpretacion_ia=respuesta["interpretacion_general"],
                         recomendacion_ia=respuesta["recomendacion"],
                         informacion_faltante_ia=respuesta["informacion_faltante"],
                         limitacion_ia=respuesta["limitacion"],
                         ia_coincide_con_nivel_esperado=respuesta["nivel_riesgo_sugerido"] == prioridad_esperada)
        documento.update(json.loads(exportar_analisis(
            reporte, hallazgos, identificador, fecha, REFERENCIA, asistido, comparacion)))
        ficha["incidencias_automaticas"] = detectar_incidencias(hallazgos, asistido, contraste, comparacion)
    except Exception as error:
        # Un fallo de un caso no interrumpe los restantes. No registrar mensajes arbitrarios,
        # cuerpos de respuesta ni razonamientos que puedan incluir datos no confiables.
        ficha["errores"].append(f"Error inesperado de ejecución ({type(error).__name__}); revisar localmente.")
    ficha["duracion_total_caso_segundos"] = round(perf_counter() - inicio, 3)
    ficha["ejecutado_correctamente"] = ficha["reglas_ejecutadas"] and ficha["respuesta_ia_valida"] and not ficha["errores"]
    documento["evaluacion"] = ficha
    return documento


def detectar_repeticiones(documentos):
    """Detectar textos exactamente iguales entre respuestas aceptadas, sin juzgar su calidad."""
    grupos = []
    for campo in ("interpretacion_ia", "recomendacion_ia"):
        indices = defaultdict(list)
        for documento in documentos:
            ficha = documento["evaluacion"]
            if ficha["respuesta_ia_valida"]:
                normalizado = " ".join(ficha[campo].casefold().split())
                indices[normalizado].append(ficha["identificador"])
        for ids in indices.values():
            if len(ids) > 1:
                grupo = {"campo": campo, "casos": ids}
                grupos.append(grupo)
                for documento in documentos:
                    ficha = documento["evaluacion"]
                    if ficha["identificador"] in ids:
                        ficha["incidencias_automaticas"].append(
                            f"Texto igual en {campo} para {', '.join(ids)}; revisar si es apropiado.")
    return grupos


def estadisticas_tiempo(valores):
    return {"cantidad": len(valores), "promedio": round(mean(valores), 3) if valores else None,
            "minimo": min(valores) if valores else None, "maximo": max(valores) if valores else None}


def tasa(valores):
    evaluables = [valor for valor in valores if valor is not None]
    return {"coincidentes": sum(evaluables), "evaluables": len(evaluables),
            "porcentaje": round(100 * sum(evaluables) / len(evaluables), 2) if evaluables else None}


def metricas(fichas):
    return {
        "total": len(fichas),
        "correctos": sum(f["ejecutado_correctamente"] for f in fichas),
        "con_errores": sum(bool(f["errores"]) for f in fichas),
        "reglas_ejecutadas": sum(f["reglas_ejecutadas"] for f in fichas),
        "respuestas_ia_validas": sum(f["respuesta_ia_valida"] for f in fichas),
        "reglas_ia": tasa([f["coinciden_reglas_ia"] for f in fichas]),
        "reglas_esperado": tasa([f["reglas_coinciden_con_esperado"] for f in fichas]),
        "ia_nivel_esperado": tasa([f["ia_coincide_con_nivel_esperado"] for f in fichas]),
        "tiempos_intentos_ia": estadisticas_tiempo([
            f["tiempo_respuesta_segundos"] for f in fichas if f["tiempo_respuesta_segundos"] is not None]),
        "tiempos_respuestas_validas": estadisticas_tiempo([
            f["tiempo_respuesta_segundos"] for f in fichas if f["respuesta_ia_valida"]]),
        "estados_ia": dict(Counter(f["estado_ia"] for f in fichas)),
        "niveles_ia_validos": dict(Counter(f["nivel_riesgo_sugerido_ia"] for f in fichas if f["respuesta_ia_valida"])),
        "discrepancias_nivel": [f["identificador"] for f in fichas if f["coinciden_reglas_ia"] is False],
        "casos_con_incidencias": sum(bool(f["incidencias_automaticas"]) for f in fichas),
    }


def celda_csv(valor):
    if valor is None:
        return ""
    if isinstance(valor, (dict, list)):
        return json.dumps(valor, ensure_ascii=False)
    if isinstance(valor, str) and valor.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + valor  # Evitar interpretar texto del modelo como fórmula en Excel.
    return valor


def escribir_csv(ruta, filas):
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows({campo: celda_csv(valor) for campo, valor in fila.items()} for fila in filas)


def escribir_json(ruta, datos):
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def texto_tasa(resultado):
    if not resultado["evaluables"]:
        return "No evaluable (0 respuestas válidas)"
    return f"{resultado['coincidentes']}/{resultado['evaluables']} ({resultado['porcentaje']:.2f} %)"


def generar_resumen(documentos, ejecucion, estado_inicial, duracion, repetidos, integridad):
    fichas = [d["evaluacion"] for d in documentos]
    general = metricas(fichas)
    lineas = [
        "# Evaluación integral del asistente", "",
        f"- Ejecución: `{ejecucion['identificador']}`.",
        f"- Inicio UTC: {ejecucion['inicio_utc']}.",
        f"- Referencia fija: `{REFERENCIA.isoformat()}`.",
        f"- Modelo: `{MODELO}`; ejecución real, secuencial, sin respuestas simuladas.",
        f"- Estado inicial de Ollama: {estado_inicial['mensaje']}",
        f"- SHA-256 del conjunto: `{ejecucion['sha256_casos']}`.",
        f"- Archivos fuente y casos sin cambios durante la evaluación: {'Sí' if integridad else 'No'}.",
        f"- Duración total del lote: {duracion:.3f} segundos.", "",
        "## Métricas automáticas", "",
        f"- Casos procesados: {general['total']}.",
        f"- Casos ejecutados correctamente (reglas + respuesta IA validada, sin errores): {general['correctos']}.",
        f"- Casos con errores: {general['con_errores']}.",
        f"- Validaciones deterministas ejecutadas: {general['reglas_ejecutadas']}.",
        f"- Respuestas de IA aceptadas por los controles existentes: {general['respuestas_ia_validas']}.",
        f"- Concordancia de niveles reglas–IA: {texto_tasa(general['reglas_ia'])}.",
        f"- Reglas frente a TODOS los hallazgos esperados: {texto_tasa(general['reglas_esperado'])}.",
        f"- IA frente a la prioridad máxima esperada (solo nivel): {texto_tasa(general['ia_nivel_esperado'])}.",
        f"- Discrepancias de nivel en respuestas válidas: {', '.join(general['discrepancias_nivel']) or 'Ninguna'}.",
        f"- Estados IA: {json.dumps(general['estados_ia'], ensure_ascii=False)}.",
        f"- Distribución de niveles IA válidos: {json.dumps(general['niveles_ia_validos'], ensure_ascii=False)}.", "",
        "## Tiempos de respuesta", "",
        "Tiempo de la llamada al módulo IA: incluye comprobación local, carga del modelo, generación y validación; no es tiempo puro de inferencia.", "",
        "| Muestra | Cantidad | Promedio (s) | Mínimo (s) | Máximo (s) |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for etiqueta, clave in (("Todos los intentos de IA", "tiempos_intentos_ia"),
                            ("Solo respuestas IA válidas", "tiempos_respuestas_validas")):
        t = general[clave]
        lineas.append(f"| {etiqueta} | {t['cantidad']} | {t['promedio']} | {t['minimo']} | {t['maximo']} |")
    lineas += ["", "## Resultados por categoría", "",
               "| Categoría | Casos | Correctos | Con errores | IA válida | Reglas–IA | Reglas–esperado | IA–nivel esperado | Promedio intento IA (s) |",
               "| --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |"]
    for categoria in ("Problematico", "Legitimo", "Ambiguo"):
        m = metricas([f for f in fichas if f["categoria"] == categoria])
        lineas.append(f"| {categoria} | {m['total']} | {m['correctos']} | {m['con_errores']} | {m['respuestas_ia_validas']} | {texto_tasa(m['reglas_ia'])} | {texto_tasa(m['reglas_esperado'])} | {texto_tasa(m['ia_nivel_esperado'])} | {m['tiempos_intentos_ia']['promedio']} |")
    lineas.append("")
    for categoria in ("Problematico", "Legitimo", "Ambiguo"):
        m = metricas([f for f in fichas if f["categoria"] == categoria])
        t = m["tiempos_intentos_ia"]
        lineas.append(f"- {categoria}: niveles IA válidos {json.dumps(m['niveles_ia_validos'], ensure_ascii=False)}; "
                      f"tiempo mínimo {t['minimo']} s, máximo {t['maximo']} s.")
    lineas += ["", "## Separación de los casos reservados", "",
               "Los 10 casos reservados se ejecutaron como evaluación final. No se ajustaron las reglas, el modelo ni sus instrucciones con los resultados de este lote.", "",
               "| Grupo | Casos | IA válida | Concordancia reglas–IA |",
               "| --- | ---: | ---: | --- |"]
    for reservado, etiqueta in ((False, "No reservados"), (True, "Reservados para evaluación final")):
        m = metricas([f for f in fichas if f["reservado_evaluacion_final"] is reservado])
        lineas.append(f"| {etiqueta} | {m['total']} | {m['respuestas_ia_validas']} | {texto_tasa(m['reglas_ia'])} |")
    lineas += ["", "## Errores e incidencias detectables automáticamente", ""]
    for ficha in fichas:
        avisos = ficha["errores"] + ficha["incidencias_automaticas"]
        for aviso in avisos:
            lineas.append(f"- {ficha['identificador']}: {aviso}")
    if not any(f["errores"] or f["incidencias_automaticas"] for f in fichas):
        lineas.append("No se detectaron incidencias con las comprobaciones implementadas.")
    lineas += ["", f"Grupos de textos repetidos entre respuestas válidas: {len(repetidos)}.", "",
               "## Interpretación y revisión humana pendiente", "",
               "- La concordancia no mide precisión independiente de la IA: el modelo recibe los hallazgos de las reglas y sus controles rechazan determinadas discrepancias. Se evalúa el sistema asistido completo, con ese sesgo de selección explícito.",
               "- Los porcentajes reglas–IA e IA–nivel esperado usan únicamente respuestas IA válidas como denominador. No se ocultan los fallos: se informan aparte. El No concluyente de reserva ante un error NO se cuenta como respuesta del modelo ni como coincidencia.",
               "- La expectativa original es un conjunto de hallazgos deterministas. Solo las reglas se contrastan con todos sus fragmentos de evidencia e interpretación; la IA se coteja únicamente con la prioridad máxima esperada. No se afirma que su texto satisfaga esa expectativa.",
               "- La prioridad máxima se obtiene del módulo existente (Alta, Media, No concluyente, Baja). En casos ambiguos puede coexistir Alta con No concluyente.",
               "- Igualdad de textos y repetición de un campo faltante son señales mecánicas: pueden ser legítimas. Las respuestas rechazadas se conservan como errores de la integración; no se guardan sus textos sin validar ni razonamientos internos.",
               "- Se marca una posible inconsistencia si la IA enumera literalmente un nombre de campo como faltante y ese campo ya tiene un valor conocido en la entrada entregada al modelo (se excluyen null y Desconocido). No se interpretan peticiones redactadas de otra manera ni se decide si estaba solicitando documentación adicional.",
               "- Pertinencia, coherencia, ausencia de contradicciones, reconocimiento de incertidumbre, utilidad y valor agregado requieren revisión semántica humana. Completar revision_humana.csv; no se asignan puntuaciones automáticamente.",
               "- Se mantienen la minimización de entrada, las instrucciones y los límites de espera actuales. El modelo no recibe identificadores, activos ni observaciones. Las entradas originales son exclusivamente los casos sintéticos oficiales.",
               "- CSV en UTF-8 con BOM. Los textos que podrían interpretarse como fórmulas se prefijan con apóstrofo solo en CSV; el JSON conserva el texto válido original.", ""]
    return "\n".join(lineas)


def ejecutar_evaluacion(salida):
    casos = cargar_casos()
    comprobar_laboratorio(casos)
    fuentes_antes = {str(p.relative_to(RAIZ)): huella(p) for p in ARCHIVOS_PROTEGIDOS}
    # Evitar sobrescribir una evaluación previa o sus anotaciones humanas.
    salida.mkdir(parents=True, exist_ok=False)
    ejecucion = {"identificador": str(uuid4()), "inicio_utc": datetime.now(timezone.utc).isoformat(),
                 "sha256_casos": huella(RUTA_CASOS), "modelo": MODELO}
    estado = comprobar_ollama()
    print(f"Ollama: {estado['mensaje']}", flush=True)
    print(f"Referencia: {REFERENCIA.isoformat()} | Modelo: {MODELO}", flush=True)
    documentos = []
    inicio = perf_counter()
    for numero, caso in enumerate(casos, 1):
        print(f"[{numero:02d}/20] {caso['identificador']} ({caso['categoria']}) iniciando…", flush=True)
        documento = evaluar_caso(caso, ejecucion)
        documentos.append(documento)
        escribir_json(salida / f"{caso['identificador']}.json", documento)
        ficha = documento["evaluacion"]
        print(f"  Reglas={ficha['prioridad_maxima_reglas']} | IA={ficha['nivel_riesgo_sugerido_ia']} "
              f"| Estado={ficha['estado_ia']} | Tiempo={ficha['tiempo_respuesta_segundos']} s "
              f"| Errores={len(ficha['errores'])}", flush=True)
    repetidos = detectar_repeticiones(documentos)
    for documento in documentos:
        escribir_json(salida / f"{documento['evaluacion']['identificador']}.json", documento)
    fichas = [d["evaluacion"] for d in documentos]
    escribir_csv(salida / "resultados.csv", fichas)
    revisiones = []
    for ficha in fichas:
        revisiones.append({
            "identificador": ficha["identificador"], "categoria": ficha["categoria"],
            "modelo_servicio": ficha["modelo_servicio"],
            "reservado_evaluacion_final": ficha["reservado_evaluacion_final"],
            "archivo_resultado": f"{ficha['identificador']}.json", "estado_ia": ficha["estado_ia"],
            "prioridad_reglas": ficha["prioridad_maxima_reglas"],
            "riesgo_ia": ficha["nivel_riesgo_sugerido_ia"],
            "estado_revision": "Pendiente" if ficha["respuesta_ia_valida"] else "Sin respuesta IA válida para revisar",
            "pertinencia_1_a_5": "", "coherencia_1_a_5": "", "valor_agregado_1_a_5": "",
            "contradice_hechos_si_no": "", "reconoce_incertidumbre_si_no": "",
            "informacion_faltante_adecuada_si_no": "", "recomendacion_util_si_no": "",
            "comentarios": "", "decision_humana": "",
        })
    escribir_csv(salida / "revision_humana.csv", revisiones)
    integridad = all(huella(RAIZ / nombre) == firma for nombre, firma in fuentes_antes.items())
    duracion = perf_counter() - inicio
    (salida / "resumen.md").write_text(generar_resumen(
        documentos, ejecucion, estado, duracion, repetidos, integridad), encoding="utf-8")
    m = metricas(fichas)
    print(f"Final: {m['correctos']}/20 correctos; {m['con_errores']} con errores. "
          f"Reglas–IA: {texto_tasa(m['reglas_ia'])}. Archivos: {salida}", flush=True)
    if not integridad:
        print("ADVERTENCIA: cambió un archivo fuente o el conjunto durante la ejecución.", flush=True)
        return 2
    return 1 if m["con_errores"] else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=RAIZ / "resultados_evaluacion",
                        help="Carpeta nueva para la ejecución; nunca sobrescribe una evaluación previa.")
    argumentos = parser.parse_args()
    try:
        return ejecutar_evaluacion(argumentos.salida.resolve())
    except FileExistsError:
        print("La carpeta de salida ya existe. Use --salida con otra carpeta nueva para preservar la evaluación anterior.", flush=True)
        return 2
    except (OSError, ValueError, KeyError) as error:
        print(f"No se pudo completar el lote ({type(error).__name__}); comprobar datos y carpeta de salida.", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
