"""Comparación descriptiva; nunca modifica hechos ni prioridades de las reglas."""

from core.analisis_ia import prioridad_maxima


def comparar_analisis(hallazgos, analisis_ia):
    prioridad = prioridad_maxima(hallazgos)
    respuesta = analisis_ia["respuesta_estructurada"]
    utilizable = analisis_ia["estado"] == "completado"
    coincide = prioridad == respuesta["nivel_riesgo_sugerido"] if utilizable else None
    if coincide is None:
        mensaje = "Sin respuesta asistida validada: no se puede establecer coincidencia."
    elif coincide:
        mensaje = "Coinciden los niveles de prioridad y riesgo; esto no certifica la interpretación ni la recuperabilidad."
    else:
        mensaje = "Existe una diferencia entre prioridad objetiva y riesgo sugerido que debe revisar una persona."
    return {
        "validacion_mediante_reglas": {
            "cantidad_hallazgos": len(hallazgos), "prioridad_maxima": prioridad,
            "principales_evidencias": [h.evidencia for h in hallazgos],
        },
        "analisis_asistido": {
            "nivel_riesgo_sugerido": respuesta["nivel_riesgo_sugerido"],
            "interpretacion": respuesta["interpretacion_general"],
            "recomendacion": respuesta["recomendacion"], "limitacion": respuesta["limitacion"],
        },
        "coinciden_niveles": coincide, "revision_humana": mensaje,
        "requiere_revision_humana": True,
    }
