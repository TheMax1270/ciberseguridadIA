"""Reglas objetivas; no certifican la recuperabilidad real del servicio."""

from datetime import datetime, timezone

from core.modelos import Hallazgo, ReporteRespaldo, normalizar_fecha


LIMITACION = (
    "Este resultado no garantiza por sí solo la recuperabilidad real del servicio; "
    "depende de la calidad y autenticidad de la evidencia suministrada."
)


def crear_hallazgo(reporte, evidencia, interpretacion, prioridad, recomendacion):
    """El identificador vincula cada hallazgo con el reporte de origen."""
    return Hallazgo(
        reporte.identificador or "Sin identificador", evidencia, interpretacion,
        prioridad, recomendacion, LIMITACION,
    )


def informacion_insuficiente(reporte, regla, campos):
    faltantes = [campo for campo in campos if getattr(reporte, campo) is None]
    if not faltantes:
        return []
    return [crear_hallazgo(
        reporte, f"{regla}: faltan {', '.join(faltantes)}.",
        "No hay información suficiente para completar esta comprobación.",
        "No concluyente", "Suministrar los campos faltantes y repetir la validación.",
    )]


def validar_estado_respaldo(reporte):
    hallazgos = informacion_insuficiente(reporte, "Estado del respaldo", ["estado_respaldo"])
    if reporte.estado_respaldo == "Fallido":
        hallazgos.append(crear_hallazgo(
            reporte, "estado_respaldo: Fallido.",
            "No existe evidencia de una copia satisfactoria.", "Alta",
            "Revisar la causa y ejecutar nuevamente el respaldo.",
        ))
    elif reporte.estado_respaldo == "Desconocido":
        hallazgos.append(crear_hallazgo(
            reporte, "estado_respaldo: Desconocido.",
            "Falta conocer el resultado del respaldo.", "No concluyente",
            "Obtener el reporte que confirme el estado del respaldo.",
        ))
    return hallazgos


def validar_completitud(reporte):
    hallazgos = informacion_insuficiente(
        reporte, "Completitud del respaldo", ["porcentaje_completitud"],
    )
    porcentaje = reporte.porcentaje_completitud
    if reporte.estado_respaldo == "Incompleto" or (porcentaje is not None and porcentaje < 100):
        evidencia = "no suministrado" if porcentaje is None else f"{porcentaje:g}%"
        hallazgos.append(crear_hallazgo(
            reporte, f"Estado: {reporte.estado_respaldo}; completitud: {evidencia}.",
            "El respaldo presenta evidencia de ejecución incompleta.", "Alta",
            "Revisar los elementos faltantes y repetir el proceso.",
        ))
    return hallazgos


def validar_antiguedad_respaldo(reporte, fecha_referencia=None):
    hallazgos = informacion_insuficiente(reporte, "Antigüedad del respaldo", [
        "fecha_respaldo", "antiguedad_maxima_respaldo_horas",
    ])
    if reporte.fecha_respaldo is None:
        return hallazgos
    referencia = obtener_referencia(fecha_referencia)
    horas = (referencia - reporte.fecha_respaldo).total_seconds() / 3600
    if horas < 0:
        hallazgos.append(fecha_futura(reporte, "fecha_respaldo"))
    elif reporte.antiguedad_maxima_respaldo_horas is not None:
        limite = reporte.antiguedad_maxima_respaldo_horas
        if horas > limite:
            hallazgos.append(crear_hallazgo(
                reporte, f"Han transcurrido {horas:.2f} horas; límite: {limite:g} horas.",
                "El respaldo supera la antigüedad máxima definida.",
                "Alta" if horas > 2 * limite else "Media",
                "Ejecutar un nuevo respaldo y revisar la frecuencia programada.",
            ))
    return hallazgos


def validar_evidencia_restauracion(reporte):
    hallazgos = informacion_insuficiente(reporte, "Evidencia de restauración", [
        "fecha_ultima_restauracion", "estado_ultima_restauracion",
    ])
    if (reporte.fecha_ultima_restauracion is None
            or reporte.estado_ultima_restauracion in (None, "Desconocido")):
        hallazgos.append(crear_hallazgo(
            reporte,
            f"Fecha de restauración: {reporte.fecha_ultima_restauracion}; "
            f"estado: {reporte.estado_ultima_restauracion}.",
            "La existencia del respaldo no demuestra recuperabilidad.", "Alta",
            "Realizar una restauración controlada en laboratorio y conservar la evidencia.",
        ))
    return hallazgos


def validar_estado_restauracion(reporte):
    if reporte.estado_ultima_restauracion == "Fallido":
        return [crear_hallazgo(
            reporte, "estado_ultima_restauracion: Fallido.",
            "La última restauración reportada falló.", "Alta",
            "Investigar el fallo antes de considerar confiable el respaldo.",
        )]
    if reporte.estado_ultima_restauracion == "Incompleto":
        return [crear_hallazgo(
            reporte, "estado_ultima_restauracion: Incompleto.",
            "La prueba incompleta no demuestra una restauración satisfactoria.", "Alta",
            "Investigar los elementos faltantes y repetir la restauración controlada.",
        )]
    return []


def validar_antiguedad_restauracion(reporte, fecha_referencia=None):
    hallazgos = informacion_insuficiente(reporte, "Antigüedad de la prueba", [
        "fecha_ultima_restauracion", "antiguedad_maxima_prueba_restauracion_dias",
    ])
    if reporte.fecha_ultima_restauracion is None:
        return hallazgos
    referencia = obtener_referencia(fecha_referencia)
    dias = (referencia - reporte.fecha_ultima_restauracion).total_seconds() / 86400
    if dias < 0:
        hallazgos.append(fecha_futura(reporte, "fecha_ultima_restauracion"))
    elif reporte.antiguedad_maxima_prueba_restauracion_dias is not None:
        limite = reporte.antiguedad_maxima_prueba_restauracion_dias
        if dias > limite:
            hallazgos.append(crear_hallazgo(
                reporte, f"Han transcurrido {dias:.2f} días; límite: {limite:g} días.",
                "La prueba de restauración supera la antigüedad máxima definida.", "Media",
                "Realizar una nueva prueba controlada y conservar la evidencia.",
            ))
    return hallazgos


def validar_tiempo_restauracion(reporte):
    hallazgos = informacion_insuficiente(reporte, "Tiempo de restauración", [
        "tiempo_restauracion_minutos", "tiempo_maximo_recuperacion_minutos",
    ])
    if hallazgos:
        return hallazgos
    tiempo = reporte.tiempo_restauracion_minutos
    limite = reporte.tiempo_maximo_recuperacion_minutos
    if tiempo > limite:
        hallazgos.append(crear_hallazgo(
            reporte, f"Restauración: {tiempo:g} minutos; máximo permitido: {limite:g} minutos.",
            "La restauración técnicamente puede existir, pero no cumple el objetivo "
            "de recuperación definido.", "Alta",
            "Revisar el procedimiento y los recursos para cumplir el tiempo máximo.",
        ))
    return hallazgos


def obtener_referencia(fecha_referencia):
    return normalizar_fecha(
        fecha_referencia if fecha_referencia is not None else datetime.now(timezone.utc)
    )


def fecha_futura(reporte, campo):
    return crear_hallazgo(
        reporte, f"{campo}: {getattr(reporte, campo).isoformat()} está en el futuro.",
        "La fecha es posterior a la referencia; no permite concluir sobre su antigüedad.",
        "No concluyente", "Verificar la fecha, la zona horaria y la referencia utilizada.",
    )


def validar_reporte(reporte: ReporteRespaldo, fecha_referencia=None) -> list[Hallazgo]:
    """Ejecutar todas las reglas usando una única referencia temporal."""
    referencia = obtener_referencia(fecha_referencia)
    hallazgos = informacion_insuficiente(reporte, "Identificación del reporte", [
        "identificador", "modelo_servicio", "activo",
    ])
    hallazgos.extend(validar_estado_respaldo(reporte))
    hallazgos.extend(validar_completitud(reporte))
    hallazgos.extend(validar_antiguedad_respaldo(reporte, referencia))
    hallazgos.extend(validar_evidencia_restauracion(reporte))
    hallazgos.extend(validar_estado_restauracion(reporte))
    hallazgos.extend(validar_antiguedad_restauracion(reporte, referencia))
    hallazgos.extend(validar_tiempo_restauracion(reporte))
    if not hallazgos:
        hallazgos.append(crear_hallazgo(
            reporte, "Las comprobaciones sobre los datos suministrados fueron satisfactorias.",
            "No se identificaron incumplimientos objetivos en los datos suministrados.",
            "Baja", "Mantener los respaldos y las pruebas controladas de restauración.",
        ))
    return hallazgos
