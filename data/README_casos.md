# Casos sintéticos de validación de respaldos

Referencia común: `2026-11-25T12:00:00` (UTC según la convención del modelo).

20 casos: 8 Problematico, 8 Legitimo y 4 Ambiguo; 10 reservados para evaluación final.

La tabla reproduce los campos del JSON; las entradas y expectativas completas están en `casos_prueba.json`.

| Identificador | Categoría | Modelo de servicio | Problema o condición evaluada | Reservado para evaluación final |
| --- | --- | --- | --- | --- |
| P01 | Problematico | Infraestructura como servicio | Respaldo fallido durante la comprobación final. | No |
| P02 | Problematico | Plataforma como servicio | Respaldo incompleto al 72 %. | No |
| P03 | Problematico | Software como servicio | Respaldo exitoso con 72 horas de antigüedad. | No |
| P04 | Problematico | Infraestructura como servicio | Respaldo exitoso sin ninguna prueba de restauración. | No |
| P05 | Problematico | Plataforma como servicio | Última restauración fallida. | Sí |
| P06 | Problematico | Software como servicio | Restauración exitosa en 240 minutos frente a un máximo de 60. | Sí |
| P07 | Problematico | Infraestructura como servicio | Última prueba de restauración realizada hace 45 días. | Sí |
| P08 | Problematico | Plataforma como servicio | Respaldo incompleto y antiguo, restauración fallida y tiempo excedido. | Sí |
| L01 | Legitimo | Software como servicio | Respaldo frecuente y restauración breve. | No |
| L02 | Legitimo | Infraestructura como servicio | Respaldo diario con prueba semanal. | No |
| L03 | Legitimo | Plataforma como servicio | Respaldo reciente y recuperación de un servicio pequeño. | No |
| L04 | Legitimo | Software como servicio | Respaldo y restauración exactamente en los límites permitidos. | No |
| L05 | Legitimo | Infraestructura como servicio | Ventana de respaldo de 48 horas y recuperación extensa permitida. | Sí |
| L06 | Legitimo | Plataforma como servicio | Respaldo cada cuatro horas y prueba de restauración reciente. | Sí |
| L07 | Legitimo | Software como servicio | Servicio con objetivo estricto de recuperación. | Sí |
| L08 | Legitimo | Infraestructura como servicio | Respaldo y prueba con márgenes amplios documentados. | Sí |
| A01 | Ambiguo | Plataforma como servicio | Restauración declarada exitosa sin fecha registrada. | No |
| A02 | Ambiguo | Software como servicio | Restauración exitosa sin duración registrada. | No |
| A03 | Ambiguo | Infraestructura como servicio | Prueba fechada con estado Desconocido y duración no registrada. | Sí |
| A04 | Ambiguo | Plataforma como servicio | Estado exitoso con cobertura no cuantificada y notas contradictorias. | Sí |

Los resultados esperados especifican todos los hallazgos mediante prioridad y fragmentos de evidencia e interpretación; no se calculan con el motor.

Los 20 casos se ejecutan para verificar coherencia. Los reservados se mantienen separados para la evaluación final y no se utilizan para ajustar reglas. Una alerta Alta puede coexistir con No concluyente en un caso ambiguo.

En A04 falta un porcentaje verificable. La contradicción en las observaciones no se interpreta automáticamente.
