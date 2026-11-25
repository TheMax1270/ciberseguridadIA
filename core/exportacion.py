"""Exportación en memoria; no escribe archivos ni realiza conexiones."""

from collections import Counter
from dataclasses import asdict
import json

from core.modelos import PRIORIDADES, normalizar_fecha


def exportar_analisis(reporte, hallazgos, identificador_analisis,
                     fecha_analisis, fecha_referencia, analisis_ia=None, comparacion=None):
    """Devolver JSON con la evidencia y todos los hallazgos."""
    entrada = asdict(reporte)
    for campo in ("fecha_respaldo", "fecha_ultima_restauracion"):
        if entrada[campo] is not None:
            entrada[campo] = entrada[campo].isoformat()
    cantidades = Counter(h.prioridad for h in hallazgos)
    resultado = {
        "identificador_analisis": identificador_analisis,
        "fecha_analisis": normalizar_fecha(fecha_analisis).isoformat(),
        "fecha_referencia": normalizar_fecha(fecha_referencia).isoformat(),
        "tipo_analisis": "Validación determinista",
        "datos_entrada": entrada,
        "hallazgos": [asdict(hallazgo) for hallazgo in hallazgos],
        "total_hallazgos": len(hallazgos),
        "cantidad_por_prioridad": {p: cantidades[p] for p in PRIORIDADES},
        "requiere_revision_humana": True,
    }
    if analisis_ia is not None:
        resultado["analisis_asistido"] = analisis_ia
        resultado["comparacion"] = comparacion
        resultado["origen_resultados"] = {
            "hallazgos": "Reglas deterministas: hechos objetivos",
            "analisis_asistido": "Modelo local: apoyo interpretativo sujeto a revisión humana",
        }
    return json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False)
