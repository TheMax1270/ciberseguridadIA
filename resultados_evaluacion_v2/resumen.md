# Reevaluación v2 de los mismos casos — no validación independiente

El prompt se ajustó después de revisar la línea base. Hubo dos intentos intermedios completos, conservados sin seleccionar respuestas por caso. Consulte comparacion_linea_base_v2.md para las mejoras, regresiones y limitaciones semánticas.

# Evaluación integral del asistente

- Ejecución: `122cec17-d382-484e-9a34-589a3279f5b1`.
- Inicio UTC: 2026-11-25T09:24:24.997303+00:00.
- Referencia fija: `2026-11-25T12:00:00+00:00`.
- Modelo: `llama3.2:3b`; ejecución real, secuencial, sin respuestas simuladas.
- Estado inicial de Ollama: Ollama local disponible.
- SHA-256 del conjunto: `b7618ce305947e0e201703bbbf85809d77f3d88ab7862e1fa04132b18fbd0edc`.
- Archivos fuente y casos sin cambios durante la evaluación: Sí.
- Duración total del lote: 103.309 segundos.

## Métricas automáticas

- Casos procesados: 20.
- Casos ejecutados correctamente (reglas + respuesta IA validada, sin errores): 20.
- Casos con errores: 0.
- Validaciones deterministas ejecutadas: 20.
- Respuestas de IA aceptadas por los controles existentes: 20.
- Concordancia de niveles reglas–IA: 15/20 (75.00 %).
- Reglas frente a TODOS los hallazgos esperados: 20/20 (100.00 %).
- IA frente a la prioridad máxima esperada (solo nivel): 15/20 (75.00 %).
- Discrepancias de nivel en respuestas válidas: P02, P04, P05, A01, A03.
- Estados IA: {"completado": 20}.
- Distribución de niveles IA válidos: {"Alta": 4, "No concluyente": 7, "Media": 1, "Baja": 8}.

## Tiempos de respuesta

Tiempo de la llamada al módulo IA: incluye comprobación local, carga del modelo, generación y validación; no es tiempo puro de inferencia.

| Muestra | Cantidad | Promedio (s) | Mínimo (s) | Máximo (s) |
| --- | ---: | ---: | ---: | ---: |
| Todos los intentos de IA | 20 | 5.163 | 3.649 | 9.284 |
| Solo respuestas IA válidas | 20 | 5.163 | 3.649 | 9.284 |

## Resultados por categoría

| Categoría | Casos | Correctos | Con errores | IA válida | Reglas–IA | Reglas–esperado | IA–nivel esperado | Promedio intento IA (s) |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| Problematico | 8 | 8 | 0 | 8 | 5/8 (62.50 %) | 8/8 (100.00 %) | 5/8 (62.50 %) | 6.113 |
| Legitimo | 8 | 8 | 0 | 8 | 8/8 (100.00 %) | 8/8 (100.00 %) | 8/8 (100.00 %) | 3.892 |
| Ambiguo | 4 | 4 | 0 | 4 | 2/4 (50.00 %) | 4/4 (100.00 %) | 2/4 (50.00 %) | 5.803 |

- Problematico: niveles IA válidos {"Alta": 4, "No concluyente": 3, "Media": 1}; tiempo mínimo 4.2 s, máximo 9.284 s.
- Legitimo: niveles IA válidos {"Baja": 8}; tiempo mínimo 3.649 s, máximo 4.045 s.
- Ambiguo: niveles IA válidos {"No concluyente": 4}; tiempo mínimo 4.7 s, máximo 7.104 s.

## Separación de los casos reservados

Se reutilizaron los 10 casos originalmente reservados tras revisar la línea base. Esta ejecución es una reevaluación; esos casos ya no constituyen una evaluación final independiente.

| Grupo | Casos | IA válida | Concordancia reglas–IA |
| --- | ---: | ---: | --- |
| No reservados | 10 | 10 | 7/10 (70.00 %) |
| Reservados para evaluación final | 10 | 10 | 8/10 (80.00 %) |

## Errores e incidencias detectables automáticamente

- P01: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- P02: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Texto igual en recomendacion_ia para P02, P05, A02, A04; revisar si es apropiado.
- P03: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P03: Texto igual en recomendacion_ia para P03, P08; revisar si es apropiado.
- P04: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- P04: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- P05: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- P05: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P05: Texto igual en recomendacion_ia para P02, P05, A02, A04; revisar si es apropiado.
- P06: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P07: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P08: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P08: Texto igual en recomendacion_ia para P03, P08; revisar si es apropiado.
- L01: Texto igual en interpretacion_ia para L01, L03, L04, L07; revisar si es apropiado.
- L01: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L02: Texto igual en interpretacion_ia para L02, L05, L06, L08; revisar si es apropiado.
- L02: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L03: Texto igual en interpretacion_ia para L01, L03, L04, L07; revisar si es apropiado.
- L03: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L04: Texto igual en interpretacion_ia para L01, L03, L04, L07; revisar si es apropiado.
- L04: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L05: Texto igual en interpretacion_ia para L02, L05, L06, L08; revisar si es apropiado.
- L05: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L06: Texto igual en interpretacion_ia para L02, L05, L06, L08; revisar si es apropiado.
- L06: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L07: Texto igual en interpretacion_ia para L01, L03, L04, L07; revisar si es apropiado.
- L07: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L08: Texto igual en interpretacion_ia para L02, L05, L06, L08; revisar si es apropiado.
- L08: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- A01: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- A01: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- A01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A02: Texto igual en recomendacion_ia para P02, P05, A02, A04; revisar si es apropiado.
- A03: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- A04: Texto igual en recomendacion_ia para P02, P05, A02, A04; revisar si es apropiado.

Grupos de textos repetidos entre respuestas válidas: 5.

## Interpretación y revisión humana pendiente

- La concordancia no mide precisión independiente de la IA: el modelo recibe los hallazgos de las reglas y sus controles rechazan determinadas discrepancias. Se evalúa el sistema asistido completo, con ese sesgo de selección explícito.
- Los porcentajes reglas–IA e IA–nivel esperado usan únicamente respuestas IA válidas como denominador. No se ocultan los fallos: se informan aparte. El No concluyente de reserva ante un error NO se cuenta como respuesta del modelo ni como coincidencia.
- La expectativa original es un conjunto de hallazgos deterministas. Solo las reglas se contrastan con todos sus fragmentos de evidencia e interpretación; la IA se coteja únicamente con la prioridad máxima esperada. No se afirma que su texto satisfaga esa expectativa.
- La prioridad máxima se obtiene del módulo existente (Alta, Media, No concluyente, Baja). En casos ambiguos puede coexistir Alta con No concluyente.
- Igualdad de textos y repetición de un campo faltante son señales mecánicas: pueden ser legítimas. Las respuestas rechazadas se conservan como errores de la integración; no se guardan sus textos sin validar ni razonamientos internos.
- Se marca una posible inconsistencia si la IA enumera literalmente un nombre de campo como faltante y ese campo ya tiene un valor conocido en la entrada entregada al modelo (se excluyen null y Desconocido). No se interpretan peticiones redactadas de otra manera ni se decide si estaba solicitando documentación adicional.
- Pertinencia, coherencia, ausencia de contradicciones, reconocimiento de incertidumbre, utilidad y valor agregado requieren revisión semántica humana. Completar revision_humana.csv; no se asignan puntuaciones automáticamente.
- Se mantienen la minimización de entrada, las instrucciones y los límites de espera actuales. El modelo no recibe identificadores, activos ni observaciones. Las entradas originales son exclusivamente los casos sintéticos oficiales.
- CSV en UTF-8 con BOM. Los textos que podrían interpretarse como fórmulas se prefijan con apóstrofo solo en CSV; el JSON conserva el texto válido original.
