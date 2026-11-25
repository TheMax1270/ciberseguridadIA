# Evaluación integral del asistente

- Ejecución: `ce03d849-2edb-4041-a1b1-75a1178b4ac5`.
- Inicio UTC: 2026-11-25T09:20:47.595932+00:00.
- Referencia fija: `2026-11-25T12:00:00+00:00`.
- Modelo: `llama3.2:3b`; ejecución real, secuencial, sin respuestas simuladas.
- Estado inicial de Ollama: Ollama local disponible.
- SHA-256 del conjunto: `b7618ce305947e0e201703bbbf85809d77f3d88ab7862e1fa04132b18fbd0edc`.
- Archivos fuente y casos sin cambios durante la evaluación: Sí.
- Duración total del lote: 148.229 segundos.

## Métricas automáticas

- Casos procesados: 20.
- Casos ejecutados correctamente (reglas + respuesta IA validada, sin errores): 16.
- Casos con errores: 4.
- Validaciones deterministas ejecutadas: 20.
- Respuestas de IA aceptadas por los controles existentes: 16.
- Concordancia de niveles reglas–IA: 16/16 (100.00 %).
- Reglas frente a TODOS los hallazgos esperados: 20/20 (100.00 %).
- IA frente a la prioridad máxima esperada (solo nivel): 16/16 (100.00 %).
- Discrepancias de nivel en respuestas válidas: Ninguna.
- Estados IA: {"completado": 16, "error": 4}.
- Distribución de niveles IA válidos: {"Alta": 8, "Baja": 8}.

## Tiempos de respuesta

Tiempo de la llamada al módulo IA: incluye comprobación local, carga del modelo, generación y validación; no es tiempo puro de inferencia.

| Muestra | Cantidad | Promedio (s) | Mínimo (s) | Máximo (s) |
| --- | ---: | ---: | ---: | ---: |
| Todos los intentos de IA | 20 | 7.408 | 5.403 | 9.074 |
| Solo respuestas IA válidas | 16 | 7.601 | 5.655 | 9.074 |

## Resultados por categoría

| Categoría | Casos | Correctos | Con errores | IA válida | Reglas–IA | Reglas–esperado | IA–nivel esperado | Promedio intento IA (s) |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| Problematico | 8 | 6 | 2 | 6 | 6/6 (100.00 %) | 8/8 (100.00 %) | 6/6 (100.00 %) | 7.401 |
| Legitimo | 8 | 8 | 0 | 8 | 8/8 (100.00 %) | 8/8 (100.00 %) | 8/8 (100.00 %) | 7.639 |
| Ambiguo | 4 | 2 | 2 | 2 | 2/2 (100.00 %) | 4/4 (100.00 %) | 2/2 (100.00 %) | 6.961 |

- Problematico: niveles IA válidos {"Alta": 6}; tiempo mínimo 5.403 s, máximo 9.074 s.
- Legitimo: niveles IA válidos {"Baja": 8}; tiempo mínimo 6.322 s, máximo 8.165 s.
- Ambiguo: niveles IA válidos {"Alta": 2}; tiempo mínimo 5.655 s, máximo 8.499 s.

## Separación de los casos reservados

Los 10 casos reservados se ejecutaron como evaluación final. No se ajustaron las reglas, el modelo ni sus instrucciones con los resultados de este lote.

| Grupo | Casos | IA válida | Concordancia reglas–IA |
| --- | ---: | ---: | --- |
| No reservados | 10 | 8 | 8/8 (100.00 %) |
| Reservados para evaluación final | 10 | 8 | 8/8 (100.00 %) |

## Errores e incidencias detectables automáticamente

- P01: Posible inconsistencia: la IA enumera como faltante el campo fecha_respaldo, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P01: Posible inconsistencia: la IA enumera como faltante el campo estado_respaldo, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P01: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P01: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo fecha_respaldo, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo estado_respaldo, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo porcentaje_completitud, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo fecha_ultima_restauracion, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo estado_ultima_restauracion, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P02: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P03: El modelo intentó reducir el riesgo indicado por las reglas.
- P03: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.
- P04: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- P04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P05: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P07: El modelo intentó reducir el riesgo indicado por las reglas.
- P07: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.
- P08: Posible inconsistencia: la IA enumera como faltante el campo tiempo_restauracion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P08: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P08: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P08: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L01: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L01: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L02: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L02: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L02: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L02: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L03: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L03: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L03: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L03: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L04: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L04: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L05: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L05: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L06: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L06: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L07: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L07: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L07: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L07: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- L08: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L08: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L08: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L08: Texto igual en recomendacion_ia para L01, L02, L03, L04, L05, L06, L07, L08; revisar si es apropiado.
- A01: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- A01: La lista de información faltante contiene textos repetidos.
- A02: El modelo sugirió Baja pese a información insuficiente.
- A02: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.
- A03: Posible inconsistencia: la IA enumera como faltante el campo fecha_ultima_restauracion, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A04: El modelo sugirió Baja pese a información insuficiente.
- A04: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.

Grupos de textos repetidos entre respuestas válidas: 1.

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
