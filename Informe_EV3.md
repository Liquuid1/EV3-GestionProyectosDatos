# Implementación y control del prototipo de analítica predictiva

Evaluación 3 · Gestión de Proyectos de Datos  
Betsabé Spring y David Zúñiga · Duoc UC

## 1. Contexto, objetivo y alcance

### 1.1. Contexto del proyecto

El proyecto aborda la identificación de posibles casos de bajo rendimiento en Matemáticas en un establecimiento escolar. Su propósito es entregar a la Unidad Técnico-Pedagógica (UTP) y a los docentes una señal que les permita priorizar qué casos revisar. El equipo pedagógico puede contrastar cada alerta con los antecedentes del estudiante y decidir si corresponde ofrecer apoyo.

En la EV1 se analizó la factibilidad del proyecto y se identificaron riesgos asociados al uso de datos estudiantiles, como la falta de representatividad, los sesgos y la exposición de información personal. En la EV2 se definieron los requerimientos, el alcance del producto mínimo viable y la planificación con CRISP-DM. La EV3 lleva ese plan a una demostración técnica local y documenta la ejecución, las decisiones y sus evidencias mediante Kanboard.

### 1.2. Objetivo de la EV3

Implementar y evaluar un prototipo de analítica predictiva que estime el riesgo de bajo rendimiento relativo en Matemáticas y permita consultar alertas explicadas en un panel web. Para ello, se busca auditar y preparar los datos, comparar modelos de clasificación, verificar el desempeño del modelo seleccionado e integrar la inferencia con la carga de archivos CSV. La evaluación también contempla el seguimiento del trabajo y el registro de las desviaciones respecto del plan.

### 1.3. Alcance ejecutado y uso previsto

La EV3 comprende la auditoría de los datos, la preparación reproducible, el entrenamiento y la evaluación del modelo, el análisis de errores y la implementación de un panel local con acceso autenticado. El panel parte vacío. Tras cargar un CSV válido desde el navegador, presenta el resumen del lote, las alertas y una ficha por estudiante con su probabilidad estimada y los aportes de las variables. Se prepararon dos lotes sintéticos para demostrar el flujo. El panel mantiene en memoria el lote vigente.

Para un primer piloto, una persona autorizada del colegio prepararía un CSV con el código interno estable, el nombre, el curso, las horas de estudio y la participación extracurricular de cada estudiante. El código y el nombre permiten identificar al estudiante durante la revisión. El modelo utiliza los otros tres campos para calcular la estimación. Antes de aplicar el flujo en el establecimiento, se requiere verificar que estas variables se puedan obtener antes de la evaluación de Matemáticas y validar el desempeño con datos del colegio.

La demostración opera mediante cargas supervisadas de CSV. La conexión con el sistema de notas, el historial de lotes, los permisos diferenciados y el despliegue institucional corresponden a una etapa posterior.

## 2. Datos y preparación

Se analizaron 10.000.000 de filas distribuidas en archivos de entrenamiento (8.000.774), validación (999.229) y prueba (999.997). Los archivos comparten 21 columnas. La lectura por bloques no detectó celdas faltantes ni coincidencias de huellas de filas completas. La ausencia de identificadores limita la comprobación de cruces al nivel de filas. Tampoco se dispone de fechas de medición, documentación de origen ni evidencia de representatividad para un establecimiento chileno.

Se mantuvieron los CSV de origen y se generaron las matrices en memoria. La etiqueta señala puntajes estrictamente inferiores a 66,57446853227711, el percentil 20 de Matemáticas calculado en entrenamiento. Su frecuencia fue 20,00 % en entrenamiento y 20,07 % en validación. El corte representa rendimiento relativo en el dataset. Para la demostración se usaron curso, horas de estudio y participación extracurricular. Se excluyeron GPA, asistencia y otros puntajes por la falta de certeza sobre cuándo se midieron. Los atributos sociodemográficos se emplearon para análisis agregados.

## 3. Modelado y evaluación

Se ajustaron tres clasificadores sobre la misma muestra reproducible de 250.000 filas, con semilla 42, y se compararon en toda la validación.

| Modelo | Precisión promedio (AP) | ROC AUC |
|---|---:|---:|
| Clasificador base | 0,2007 | 0,5000 |
| Regresión logística | 0,4002 | 0,7267 |
| Árbol de decisión | 0,3891 | 0,7260 |

Se eligió la regresión logística por su mayor precisión promedio. En validación se fijó un umbral de 0,18695, maximizando precisión entre los puntos con recall de al menos 70 %. En prueba, con el umbral congelado, el modelo obtuvo AP de 0,4014, ROC AUC de 0,7279, precisión de 32,06 %, recall de 70,17 % y F1 de 0,4402.

| Resultado en prueba | Sin alerta | Con alerta |
|---|---:|---:|
| Sin bajo rendimiento según la etiqueta | 503.496 | 296.845 |
| Con bajo rendimiento según la etiqueta | 59.550 | 140.106 |

El modelo generó 436.951 alertas, un 43,70 % de prueba. La sensibilidad alcanzada implica una carga alta de revisión y todavía se omiten casos positivos. El análisis agregado por género, categoría racial y cuartil socioeconómico mostró recuentos y tasas de detección comparables dentro de los archivos. El recall por categoría racial varió entre 69,96 % y 71,43 %. Esta comparación depende de cómo se construyeron los datos y no demuestra equidad en un contexto escolar real.

Las contribuciones de Shapley de la regresión logística se calcularon en escala logit con una referencia marginal de entrenamiento. Las horas de estudio tuvieron la mayor contribución media absoluta en la muestra de explicaciones. En cada caso la suma de los aportes y la referencia reconstruye la salida del modelo. Las contribuciones describen cómo opera el modelo y no identifican efectos causales.

## 4. Implementación y verificación

El notebook de modelado exporta el escalado, los coeficientes, el intercepto, la referencia explicativa y el umbral. El script de inferencia valida el CSV, asigna identificadores por fila y escribe un JSON con probabilidades, alertas y aportes. El panel lee ese archivo y ofrece cifras agregadas y consulta individual. El acceso requiere credenciales de demostración y el servidor se vincula a la dirección local.

Se procesaron cinco registros sintéticos con dos alertas. Se comprobó el rechazo de un archivo sin una columna requerida y de otro con horas negativas, preservando la salida anterior. El controlador HTTP devolvió 401 sin credenciales y 200 con credenciales para los cinco registros, con probabilidades concordantes con el JSON. Las solicitudes se simularon en memoria porque el entorno bloquea sockets locales. La prueba en navegador confirmó el resumen de cinco registros y dos alertas. La ficha R00002 muestra una probabilidad estimada de 33,15 % y el aporte de cada predictor.

El prototipo se amplió con una carga de CSV autenticada desde el navegador. Cada carga válida reemplaza el lote vigente en memoria. El archivo incluye el código interno estable y el nombre para que el equipo pedagógico pueda identificar al estudiante. Estos campos son datos de identificación en el panel. El modelo usa curso, horas de estudio y participación extracurricular. La prueba del controlador confirmó el cambio entre dos lotes sintéticos con los mismos estudiantes y cantidades distintas de alertas. El historial de cargas y los permisos diferenciados quedan pendientes para un piloto.

## 5. Seguimiento y control

| Paquete EV2 | Trabajo de EV3 | Evidencia |
|---|---|---|
| 1.1 Inicio y planificación | Alcance definido y tareas de Kanboard registradas. | Alcance y captura inicial. |
| 1.2–1.3 Datos | Auditoría y preparación reproducible. | Notebooks 01 y 02. |
| 1.4–1.5 Modelo | Comparación, prueba, explicaciones y evaluación por grupo. | Notebook 03 y segundo reporte. |
| 1.6–1.7 Integración y dashboard | Inferencia por lotes, acceso local y revisión de resultados. | Carpeta Prototipo. |
| 1.8 Pruebas y entrega | Verificación del flujo y preparación del informe. | Bitácora e informe. |

Kanboard registró un primer ciclo de alcance y auditoría, seguido por un segundo ciclo de modelado. En la captura 05 aparecen diez tarjetas en Done, inferencia en Ready y dashboard, pruebas e informe en Backlog. La bitácora conserva ese estado observado y registra por separado la ejecución posterior. Las capturas y los reportes documentan el avance. Falta consolidar estimaciones y esfuerzo efectivamente registrado para calcular diferencias cuantitativas.

| Desviación o hallazgo | Acción adoptada | Limitación restante |
|---|---|---|
| Volumen de los CSV | Lectura por bloques y muestra reproducible para el ajuste. | Evaluar si ampliar la muestra mejora el desempeño. |
| Entorno inicial sin scikit-learn | Reutilización de un entorno local con la dependencia disponible. | Replicar el entorno si se necesita volver a entrenar. |
| Falta de fechas y procedencia verificable | Priorizar predictores plausibles y establecer una etiqueta relativa. | Validar la anticipación temporal y el contexto escolar. |
| Infraestructura institucional prevista | Integración local con Python y autenticación de demostración. | Despliegue, permisos por perfil, cifrado y validación institucional. |
| Alta carga de alertas | Justificar el umbral y comunicar su desempeño y volumen. | Acordar con UTP una capacidad de revisión y contrastar otras reglas. |

## 6. Conclusiones y próximos pasos

El flujo transforma un lote válido en alertas que pueden revisarse junto con una explicación individual. La regresión logística mejora la precisión promedio frente al clasificador base, pero el volumen de falsas alarmas limita el uso pedagógico. Antes de un piloto se requiere validar la disponibilidad temporal de los predictores, contrastar el modelo con datos de la institución y acordar un proceso de revisión humana.

Evidencias para la entrega: carpeta `Notebooks`, carpeta `Prototipo`, bitácora y reportes en `Imagenes Tablero Avance del proyecto`. La captura 05 respalda el último estado observado de Kanboard. El acceso directo al tablero local requiere el entorno del equipo.

## Anexo A. Evidencia del tablero

![Kanboard al cierre del modelado](Imagenes%20Tablero%20Avance%20del%20proyecto/05_backlog_integracion.png)

Figura 1. Diez tarjetas cerradas y trabajo de integración registrado antes de ejecutar la demo.

## Anexo B. Evidencia del prototipo

![Dashboard validado en navegador](Imagenes%20Tablero%20Avance%20del%20proyecto/06_dashboard_validado.png)

Figura 2. Lote sintético y detalle de una alerta. El 40 % corresponde al lote de demostración. El 43,70 % informado en la evaluación corresponde al conjunto de prueba.

[Notebook de auditoría](Notebooks/01_comprension_y_eda.ipynb) · [Preparación](Notebooks/02_preparacion_y_pipeline.ipynb) · [Modelado y evaluación](Notebooks/03_modelado_y_validacion.ipynb) · [Bitácora](Imagenes%20Tablero%20Avance%20del%20proyecto/bitacora_tablero.md) · [Instrucciones de la demo](Prototipo/README.md)
