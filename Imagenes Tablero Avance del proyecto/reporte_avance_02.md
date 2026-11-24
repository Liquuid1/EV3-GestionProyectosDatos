# Segundo reporte de avance de EV3

| Tarjeta | Ejecución y evidencia |
|---|---|
| #5 · Entorno | El Python inicial carecía de scikit-learn y la instalación falló. Se reutilizó un entorno local con scikit-learn 1.9.1. |
| #6 · Comparación | Se ajustaron un clasificador base, una regresión logística y un árbol con la misma muestra reproducible de 250.000 filas de entrenamiento. Se compararon sobre toda la validación. |
| #7 · Selección | La regresión logística obtuvo la mayor precisión promedio en validación (0,4002). El umbral de probabilidad de 0,18695 maximiza precisión con un recall mínimo de 70 % en validación. |
| #8 · Prueba | Recall de 70,17 %, precisión de 32,06 %, F1 de 0,4402 y tasa de alertas de 43,70 %. La matriz registra 296.845 falsas alarmas y 59.550 casos positivos omitidos. |
| #9 · Equidad y explicabilidad | Auditoría agregada y cálculo de valores de Shapley para el modelo lineal, en escala logit y con referencia marginal de entrenamiento. |
| #10 · Reporte | Este documento y las salidas del notebook de modelado. |

La tasa de alertas indica la carga que tendría que revisar un equipo pedagógico. Antes de considerar un uso institucional se requiere comprobar la disponibilidad previa de las variables y validar la capacidad para revisar alertas. Para la demostración se conserva el umbral fijado antes de usar prueba y se informa su carga de revisión.

[Evidencia técnica](../Notebooks/03_modelado_y_validacion.ipynb)
