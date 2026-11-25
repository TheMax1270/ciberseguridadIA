# Evaluación integral del asistente

- Ejecución: `56ca74c5-2161-4681-bb6f-3ad5deecfb83`.
- Inicio UTC: 2026-11-25T09:17:37.935190+00:00.
- Referencia fija: `2026-11-25T12:00:00+00:00`.
- Modelo: `llama3.2:3b`; ejecución real, secuencial, sin respuestas simuladas.
- Estado inicial de Ollama: Ollama local disponible.
- SHA-256 del conjunto: `b7618ce305947e0e201703bbbf85809d77f3d88ab7862e1fa04132b18fbd0edc`.
- Archivos fuente y casos sin cambios durante la evaluación: Sí.
- Duración total del lote: 136.879 segundos.

## Métricas automáticas

- Casos procesados: 20.
- Casos ejecutados correctamente (reglas + respuesta IA validada, sin errores): 17.
- Casos con errores: 3.
- Validaciones deterministas ejecutadas: 20.
- Respuestas de IA aceptadas por los controles existentes: 17.
- Concordancia de niveles reglas–IA: 13/17 (76.47 %).
- Reglas frente a TODOS los hallazgos esperados: 20/20 (100.00 %).
- IA frente a la prioridad máxima esperada (solo nivel): 13/17 (76.47 %).
- Discrepancias de nivel en respuestas válidas: P07, L02, L05, L08.
- Estados IA: {"completado": 17, "error": 3}.
- Distribución de niveles IA válidos: {"Alta": 12, "Baja": 5}.

## Tiempos de respuesta

Tiempo de la llamada al módulo IA: incluye comprobación local, carga del modelo, generación y validación; no es tiempo puro de inferencia.

| Muestra | Cantidad | Promedio (s) | Mínimo (s) | Máximo (s) |
| --- | ---: | ---: | ---: | ---: |
| Todos los intentos de IA | 20 | 6.841 | 4.956 | 11.169 |
| Solo respuestas IA válidas | 17 | 6.909 | 4.956 | 11.169 |

## Resultados por categoría

| Categoría | Casos | Correctos | Con errores | IA válida | Reglas–IA | Reglas–esperado | IA–nivel esperado | Promedio intento IA (s) |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| Problematico | 8 | 7 | 1 | 7 | 6/7 (85.71 %) | 8/8 (100.00 %) | 6/7 (85.71 %) | 6.798 |
| Legitimo | 8 | 8 | 0 | 8 | 5/8 (62.50 %) | 8/8 (100.00 %) | 5/8 (62.50 %) | 6.695 |
| Ambiguo | 4 | 2 | 2 | 2 | 2/2 (100.00 %) | 4/4 (100.00 %) | 2/2 (100.00 %) | 7.219 |

- Problematico: niveles IA válidos {"Alta": 7}; tiempo mínimo 4.956 s, máximo 11.169 s.
- Legitimo: niveles IA válidos {"Baja": 5, "Alta": 3}; tiempo mínimo 5.633 s, máximo 7.96 s.
- Ambiguo: niveles IA válidos {"Alta": 2}; tiempo mínimo 6.07 s, máximo 7.82 s.

## Separación de los casos reservados

Los 10 casos reservados se ejecutaron como evaluación final. No se ajustaron las reglas, el modelo ni sus instrucciones con los resultados de este lote.

| Grupo | Casos | IA válida | Concordancia reglas–IA |
| --- | ---: | ---: | --- |
| No reservados | 10 | 9 | 8/9 (88.89 %) |
| Reservados para evaluación final | 10 | 8 | 5/8 (62.50 %) |

## Errores e incidencias detectables automáticamente

- P04: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- P04: Texto igual en recomendacion_ia para P04, A01; revisar si es apropiado.
- P05: El modelo intentó reducir el riesgo indicado por las reglas.
- P05: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.
- P06: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P07: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- P08: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- P08: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L01: Texto igual en recomendacion_ia para L01, L03, L04, L06, L07; revisar si es apropiado.
- L02: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- L02: Texto igual en recomendacion_ia para L02, L05, L08; revisar si es apropiado.
- L03: Texto igual en recomendacion_ia para L01, L03, L04, L06, L07; revisar si es apropiado.
- L04: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L04: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L04: Texto igual en recomendacion_ia para L01, L03, L04, L06, L07; revisar si es apropiado.
- L05: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- L05: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L05: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L05: Texto igual en recomendacion_ia para L02, L05, L08; revisar si es apropiado.
- L06: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L06: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- L06: Texto igual en recomendacion_ia para L01, L03, L04, L06, L07; revisar si es apropiado.
- L07: Texto igual en recomendacion_ia para L01, L03, L04, L06, L07; revisar si es apropiado.
- L08: Discrepancia entre prioridad de reglas y nivel sugerido por IA.
- L08: Texto igual en recomendacion_ia para L02, L05, L08; revisar si es apropiado.
- A01: Posible solapamiento: fecha_ultima_restauracion figura como ausente en 2 reglas; puede ser legítimo.
- A01: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A01: Texto igual en recomendacion_ia para P04, A01; revisar si es apropiado.
- A02: El modelo sugirió Baja pese a información insuficiente.
- A02: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.
- A03: Posible inconsistencia: la IA enumera como faltante el campo tiempo_maximo_recuperacion_minutos, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A03: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_respaldo_horas, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A03: Posible inconsistencia: la IA enumera como faltante el campo antiguedad_maxima_prueba_restauracion_dias, pero tiene un valor suministrado. Revisar si solicita evidencia adicional.
- A04: El modelo sugirió Baja pese a información insuficiente.
- A04: IA sin respuesta validada: no atribuir su resultado de reserva al modelo.

Grupos de textos repetidos entre respuestas válidas: 3.

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
