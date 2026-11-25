"""Datos estructurados. None significa información no suministrada."""

from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite


MODELOS_SERVICIO = (
    "Infraestructura como servicio",
    "Plataforma como servicio",
    "Software como servicio",
)
ESTADOS = ("Exitoso", "Fallido", "Incompleto", "Desconocido")
PRIORIDADES = ("Alta", "Media", "Baja", "No concluyente")


def normalizar_fecha(fecha: datetime) -> datetime:
    """Aceptar datetime; interpretar fechas sin zona como UTC y convertir a UTC."""
    if not isinstance(fecha, datetime):
        raise ValueError("La fecha debe ser un datetime válido.")
    if fecha.tzinfo is None or fecha.utcoffset() is None:
        return fecha.replace(tzinfo=timezone.utc)
    return fecha.astimezone(timezone.utc)


@dataclass(frozen=True)
class ReporteRespaldo:
    identificador: str | None = None
    modelo_servicio: str | None = None
    activo: str | None = None
    fecha_respaldo: datetime | None = None
    estado_respaldo: str | None = None
    porcentaje_completitud: float | None = None
    fecha_ultima_restauracion: datetime | None = None
    estado_ultima_restauracion: str | None = None
    tiempo_restauracion_minutos: float | None = None
    tiempo_maximo_recuperacion_minutos: float | None = None
    antiguedad_maxima_respaldo_horas: float | None = None
    antiguedad_maxima_prueba_restauracion_dias: float | None = None
    observaciones: str | None = None

    def __post_init__(self):
        for campo in ("identificador", "activo", "observaciones"):
            valor = getattr(self, campo)
            if valor is not None and not isinstance(valor, str):
                raise ValueError(f"{campo} debe ser texto o None.")
            if isinstance(valor, str):
                object.__setattr__(self, campo, valor.strip() or None)

        for campo, opciones in (
            ("modelo_servicio", MODELOS_SERVICIO),
            ("estado_respaldo", ESTADOS),
            ("estado_ultima_restauracion", ESTADOS),
        ):
            valor = getattr(self, campo)
            if valor is not None and valor not in opciones:
                raise ValueError(f"{campo}: valor no permitido: {valor!r}.")

        for campo in ("fecha_respaldo", "fecha_ultima_restauracion"):
            valor = getattr(self, campo)
            if valor is not None:
                object.__setattr__(self, campo, normalizar_fecha(valor))

        for campo in (
            "porcentaje_completitud",
            "tiempo_restauracion_minutos",
            "tiempo_maximo_recuperacion_minutos",
            "antiguedad_maxima_respaldo_horas",
            "antiguedad_maxima_prueba_restauracion_dias",
        ):
            valor = getattr(self, campo)
            if valor is None:
                continue
            if (isinstance(valor, bool) or not isinstance(valor, (int, float))
                    or not isfinite(valor) or valor < 0):
                raise ValueError(f"{campo} debe ser un número finito no negativo.")
            if campo == "porcentaje_completitud" and valor > 100:
                raise ValueError("porcentaje_completitud debe estar entre 0 y 100.")


@dataclass(frozen=True)
class Hallazgo:
    identificador: str
    evidencia: str
    interpretacion: str
    prioridad: str
    recomendacion: str
    limitacion: str

    def __post_init__(self):
        if self.prioridad not in PRIORIDADES:
            raise ValueError(f"Prioridad no permitida: {self.prioridad!r}.")
