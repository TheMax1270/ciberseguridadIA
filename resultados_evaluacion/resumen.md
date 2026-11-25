# Evaluación integral del asistente

- Ejecución: `67c60c1e-7480-4208-b657-cd12baa2ae11`.
- Inicio UTC: 2026-11-25T08:31:44.328462+00:00.
- Referencia fija: `2026-11-25T12:00:00+00:00`.
- Modelo: `llama3.2:3b`; ejecución real, secuencial, sin respuestas simuladas.
- Estado inicial de Ollama: Ollama local disponible.
- SHA-256 del conjunto: `b7618ce305947e0e201703bbbf85809d77f3d88ab7862e1fa04132b18fbd0edc`.
- Archivos fuente y casos sin cambios durante la evaluación: Sí.
- Duración total del lote: 125.975 segundos.

## Métricas automáticas

- Casos procesados: 20.
- Casos ejecutados correctamente (reglas + respuesta IA validada, sin errores): 20.
- Casos con errores: 0.
- Validaciones deterministas ejecutadas: 20.
- Respuestas de IA aceptadas por los controles existentes: 20.
- Concordancia de niveles reglas–IA: 15/20 (75.00 %).
- Reglas frente a TODOS los hallazgos esperados: 20/20 (100.00 %).
- IA frente a la prioridad máxima esperada (solo nivel): 15/20 (75.00 %).
- Discrepancias de nivel en respuestas válidas: A02, A04, L02, L04, P07.
- Estados IA: {"completado": 20}.
- Distribución de niveles IA válidos: {"Alta": 14, "Baja": 6}.

## Tiempos de respuesta

Tiempo de la llamada al módulo IA: incluye comprobación local, carga del modelo, generación y validación; no es tiempo puro de inferencia.

| Muestra | Cantidad | Promedio (s) | Mínimo (s) | Máximo (s) |
| --- | ---: | ---: | ---: | ---: |
| Todos los intentos de IA | 20 | 6.296 | 4.872 | 8.087 |
| Solo respuestas IA válidas | 20 | 6.296 | 4.872 | 8.087 |

## Resultados por categoría

| Categoría | Casos | Correctos | Con errores | IA válida | Reglas–IA | Reglas–esperado | IA–nivel esperado | Promedio intento IA (s) |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| Problematico | 8 | 8 | 0 | 8 | 7/8 (87.50 %) | 8/8 (100.00 %) | 7/8 (87.50 %) | 6.241 |
| Legitimo | 8 | 8 | 0 | 8 | 6/8 (75.00 %) | 8/8 (100.00 %) | 6/8 (75.00 %) | 6.115 |
| Ambiguo | 4 | 4 | 0 | 4 | 2/4 (50.00 %) | 4/4 (100.00 %) | 2/4 (50.00 %) | 6.768 |

- Problematico: niveles IA válidos {"Alta": 8}; tiempo mínimo 4.872 s, máximo 8.087 s.
- Legitimo: niveles IA válidos {"Baja": 6, "Alta": 2}; tiempo mínimo 5.891 s, máximo 6.384 s.
- Ambiguo: niveles IA válidos {"Alta": 4}; tiempo mínimo 6.263 s, máximo 7.126 s.

## Separación de los casos reservados

Los 10 casos reservados se ejecutaron como evaluación final. No se ajustaron las reglas, el modelo ni sus instrucciones con los resultados de este lote.

| Grupo | Casos | IA válida | Concordancia reglas–IA |
| --- | ---: | ---: | --- |
| No reservados | 10 | 10 | 7/10 (70.00 %) |
| Reservados para evaluación final | 10 | 10 | 8/10 (80.00 %) |

## Errores e incidencias detectables automáticamente

- A01: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- A01: La lista de información faltante contiene textos repetidos.
- A01: Texto igual en recomendacion_ia para A01, P04; revisar si es apropiado.
- A02: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- A02: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A02: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A02: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A04: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- A04: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A04: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L01: La lista de información faltante contiene textos repetidos.
- L01: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L02: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- L02: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L03: Texto igual en interpretacion_ia para L03, L06; revisar si es apropiado.
- L03: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L04: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- L04: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L05: Texto igual en interpretacion_ia para L05, L08; revisar si es apropiado.
- L05: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L06: La lista de información faltante contiene textos repetidos.
- L06: Texto igual en interpretacion_ia para L03, L06; revisar si es apropiado.
- L06: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- L07: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L07: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L07: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L08: La lista de información faltante contiene textos repetidos.
- L08: Texto igual en interpretacion_ia para L05, L08; revisar si es apropiado.
- L08: Texto igual en recomendacion_ia para A04, L01, L02, L03, L04, L05, L06, L08; revisar si es apropiado.
- P01: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P04: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- P04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P04: Texto igual en recomendacion_ia para A01, P04; revisar si es apropiado.
- P05: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P07: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- P07: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P07: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P07: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.

Grupos de textos repetidos entre respuestas válidas: 4.

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

## Trazabilidad del posprocesamiento

Controles automáticos adicionales sobre las mismas respuestas reales; sin repetir inferencias ni modificar el modelo.

SHA-256 del evaluador utilizado en la consolidación: `fe9deabd2f9bf9af0cc2d28e590fe6046fc0ca579d4f0b94a6a418da576c3f33`.
