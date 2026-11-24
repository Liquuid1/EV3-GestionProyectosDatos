# Primer reporte de avance de EV3

| Tarjeta | Plan | Evidencia del trabajo |
|---|---|---|
| #1 · Alcance | Definir los entregables de EV3 y su relación con EV2. | [Alcance documentado](alcance_ev3.md). La segunda captura muestra Done. |
| #2 · Auditoría | Revisar esquema, volumen, calidad, duplicados y cruces entre archivos. | [Notebook ejecutado](../Notebooks/01_comprension_y_eda.ipynb). Se procesaron 10 millones de registros en tres CSV de 21 columnas. |
| #3 · Etiqueta y predictores | Definir el rendimiento bajo y las variables disponibles para estimarlo. | Propuesta documentada en el notebook. Usa el percentil 20 de entrenamiento, con corte mostrado de 66,57, y tres predictores candidatos. |
| #4 · Reporte de avance | Registrar trabajo, riesgos y decisiones. | Este reporte y la [bitácora](bitacora_tablero.md). |

La auditoría no detectó faltantes ni huellas de filas completas repetidas. El tamaño de los CSV se manejó con lectura por bloques. La falta de documentación de origen y de fechas limita la interpretación del modelo. Se excluyeron de la propuesta GPA, los puntajes de otras materias y la asistencia mientras no se pueda verificar su disponibilidad previa.

La segunda captura precede al cierre técnico de la auditoría. La bitácora conserva ese estado como evidencia del tablero. El siguiente corte debe reflejar el cierre de #2, la revisión de la propuesta de #3 y la incorporación de este reporte a #4. Sigue la preparación reproducible de los tres conjuntos y la comparación de modelos usando validación.

La preparación posterior confirmó la definición operativa de la tarjeta #3. El percentil 20 exacto de entrenamiento es 66,57446853227711. La misma regla de etiquetado da un 20,07 % de clase positiva en validación. El [notebook de preparación](../Notebooks/02_preparacion_y_pipeline.ipynb) conserva el código y los resultados.
