"""Lectura local de casos oficiales y conversión de fechas ISO."""

from datetime import datetime
import json
from pathlib import Path

from core.modelos import ReporteRespaldo

RUTA_CASOS = Path(__file__).resolve().parents[1] / "data" / "casos_prueba.json"


def cargar_casos(ruta=RUTA_CASOS):
    with Path(ruta).open(encoding="utf-8") as archivo:
        return json.load(archivo)["casos"]


def convertir_entrada(entrada):
    datos = dict(entrada)
    for campo in ("fecha_respaldo", "fecha_ultima_restauracion"):
        if isinstance(datos.get(campo), str):
            datos[campo] = datetime.fromisoformat(datos[campo])
    return ReporteRespaldo(**datos)
