# Comparación: línea base y reevaluación v2

**Esta es una reevaluación de los mismos 20 casos después de revisar sus resultados; no es una validación independiente.** Los casos originalmente reservados también fueron reutilizados y ya no constituyen un conjunto inédito.

Solo se modificó INSTRUCCIONES_SISTEMA. No cambiaron las reglas, el evaluador, la interfaz, los controles de salida, las opciones de generación, el modelo configurado, el esquema ni los casos. La integridad de los 23 archivos de la línea base se comprobó con SHA-256.

Se hicieron dos intentos intermedios completos y un lote final de 20 casos. Todos se conservan; no se combinaron ni seleccionaron respuestas favorables por caso. Los tiempos son observaciones de ejecución local, no un experimento de rendimiento controlado.

## Métricas automáticas

| Indicador | Línea base | v2 final |
| --- | ---: | ---: |
| Casos procesados / respuestas aceptadas | 20 / 20 | 20 / 20 |
| Casos con errores técnicos o rechazos | 0 | 0 |
| Concordancia de niveles reglas–IA | 15/20 (75.0 %) | 15/20 (75.0 %) |
| Reglas frente a todos los hallazgos esperados | 100.0 % | 100.0 % |
| IA frente al nivel máximo esperado, solo etiqueta | 75.0 % | 75.0 % |
| Legítimos etiquetados Alta | 2 | 0 |
| Casos que solicitan literalmente campos ya conocidos | 8 | 8 |
| Menciones de campos ya conocidos en esas listas | 21 | 8 |
| Casos con información faltante duplicada | 4 | 0 |
| Tiempo promedio de todos los intentos (s) | 6.296 | 5.163 |
| Tiempo mínimo / máximo (s) | 4.872 / 8.087 | 3.649 / 9.284 |

**La concordancia no es precisión independiente de la IA ni certifica su texto.** El modelo recibe los hallazgos y los controles existentes condicionan las respuestas aceptadas. Una aceptación estructural tampoco demuestra corrección semántica.

## Por categoría

| Categoría | Base: concordancia / errores | v2: concordancia / errores |
| --- | --- | --- |
| Problematico | 7/8 / 0 | 5/8 / 0 |
| Legitimo | 6/8 / 0 | 8/8 / 0 |
| Ambiguo | 2/4 / 0 | 2/4 / 0 |

## Discrepancias, sin ocultar regresiones

- Línea base: A02, A04, L02, L04, P07.
- v2 final: A01, A03, P02, P04, P05.
- Las discrepancias de la línea base cambiaron a coincidencia en v2: A02, A04, L02, L04, P07.
- Aparecieron nuevas discrepancias en v2: A01, A03, P02, P04, P05.
- Campos conocidos solicitados, base: A02, A04, L07, P01, P04, P05, P06, P07.
- Campos conocidos solicitados, v2: A01, P01, P02, P03, P05, P06, P07, P08.

## Revisión cualitativa de muestras: mejoras y problemas pendientes

- A02: v2 distingue duración desconocida de fallo demostrado y propone registrarla; el nivel pasa de Alta a No concluyente. Esto está sustentado en que tiempo_restauracion_minutos realmente es null.
- P07: v2 atribuye la antigüedad a la prueba de restauración y sugiere Media. La interpretación es más precisa que la mezcla de respaldo y prueba en la línea base, pero todavía solicita una duración que ya estaba suministrada.
- P01: v2 menciona una copia anterior exitosa no identificada explícitamente en los datos y afirma que no se identifican incumplimientos objetivos pese a describir un respaldo fallido. Su etiqueta Alta coincide, pero el texto es contradictorio; la coincidencia no acredita calidad.
- P02: v2 menciona una duración de 20 minutos y luego dice que no se conoce. Pasa a No concluyente pese al respaldo incompleto demostrado. Es una regresión semántica, no una corrección de sobreestimación.
- P05: v2 reconoce la restauración fallida pero inventa que su duración falta y orienta la recomendación a registrarla. La restauración tiene tiempo_restauracion_minutos=20; investigar el fallo sigue siendo necesario.
- A04: la lista identifica porcentaje_completitud como faltante, pero la interpretación y recomendación hablan de una duración desconocida cuando se suministraron 20 minutos. La plantilla del ejemplo temporal parece haber influido en un caso diferente; es una observación compatible con transferencia indebida del ejemplo, no una explicación causal demostrada.
- P08: la recomendación de registrar una duración ya conocida no cubre adecuadamente los problemas simultáneos. Persisten recomendaciones imprecisas.
- Los ejemplos genéricos del prompt no contienen identificadores ni respuestas oficiales, pero pueden inducir repetición de plantillas. No se considera resuelto el objetivo de interpretación específica por haber eliminado duplicados en una lista.

Estas son observaciones sobre textos reales, no una puntuación humana sistemática de los 20 casos. revision_humana.csv sigue sin calificaciones automáticas. No se puede afirmar una mejora semántica uniforme ni la corrección completa de los cinco problemas con este ajuste.

## Intentos intermedios conservados

| Lote | Válidas | Errores | Concordancia solo en válidas | Coincidencias sobre los 20 intentos | Carpeta |
| --- | ---: | ---: | --- | --- | --- |
| intermedio_1 | 17 | 3 | 13/17 (76.47 %) | 13/20 (65.00 %) | resultados_evaluacion_v2_intento_intermedio |
| intermedio_2 | 16 | 4 | 16/16 (100.0 %) | 16/20 (80.00 %) | resultados_evaluacion_v2_intento_intermedio_2 |
| v2 | 20 | 0 | 15/20 (75.0 %) | 15/20 (75.00 %) | resultados_evaluacion_v2 |

### Errores de intermedio_1

- A02: El modelo sugirió Baja pese a información insuficiente.
- A04: El modelo sugirió Baja pese a información insuficiente.
- P05: El modelo intentó reducir el riesgo indicado por las reglas.

### Errores de intermedio_2

- A02: El modelo sugirió Baja pese a información insuficiente.
- A04: El modelo sugirió Baja pese a información insuficiente.
- P03: El modelo intentó reducir el riesgo indicado por las reglas.
- P07: El modelo intentó reducir el riesgo indicado por las reglas.

El 100 % del segundo intento intermedio solo correspondió a 16 respuestas aceptadas; hubo cuatro rechazos. No se presenta como éxito global ni como validación del modelo. Los textos rechazados siguen sin almacenarse por los mecanismos de privacidad existentes.

## Integridad y pruebas

- SHA-256: los 23 archivos de la línea base permanecen idénticos byte por byte.
- AST de core/analisis_ia.py: idéntico salvo INSTRUCCIONES_SISTEMA. Todos los demás archivos fuente auditados, tests, interfaz, evaluador y casos conservan sus hashes.
- Se mantuvieron llama3.2:3b, la ejecución secuencial, las opciones de generación, la referencia UTC y los controles de privacidad. El digest local del modelo no cambió entre el inicio y el cierre de este trabajo; la línea base antigua no registró digest y no permite certificar igualdad criptográfica de pesos retrospectivamente.
- Suite final: Ran 78 tests in 3.615s — OK.
- auditoria_prompt.json conserva prompts de la línea base, ambos intentos y versión final, junto con hashes, estados y métricas.
