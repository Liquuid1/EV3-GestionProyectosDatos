# Seguimiento académico en Matemáticas · EV3

Prototipo académico para estimar el riesgo de bajo rendimiento relativo en Matemáticas. El panel permite cargar un CSV y revisar alertas, probabilidades y aportes por variable. Las alertas requieren revisión pedagógica.

## Ejecutar la demostración

Descarga o clona el repositorio y abre una terminal en su raíz. La demo usa la biblioteca estándar de **Python 3.10 o posterior** e incluye el modelo entrenado y dos lotes sintéticos. No requiere instalar paquetes, descargar los CSV de entrenamiento ni reentrenar el modelo.

| Sistema | Comando |
|---|---|
| Windows | `py -3 Prototipo/dashboard.py` |
| macOS o Linux | `python3 Prototipo/dashboard.py` |

1. Escribe una contraseña para esta sesión cuando la terminal la solicite.
2. Abre [el panel local](http://127.0.0.1:8765/) e inicia sesión con el usuario `demo` y la contraseña que elegiste.
3. Carga [lote_demo.csv](Prototipo/lote_demo.csv). Deben aparecer **cinco registros y dos alertas**.
4. Carga [lote_demo_b.csv](Prototipo/lote_demo_b.csv). Aparecerán los mismos cinco identificadores con **una alerta**.

El servidor parte vacío. Cada carga válida reemplaza el lote vigente en memoria. El panel usa el código interno y el nombre para la consulta. El modelo utiliza únicamente el curso, las horas de estudio y la participación extracurricular. Usa datos sintéticos para la demo. Detén el servidor con Ctrl+C.

## Reproducir el análisis y el entrenamiento

El entorno de referencia para los notebooks usa Python 3.14.10. Descarga los CSV de [Student Performance en Kaggle](https://www.kaggle.com/datasets/neuralsorcerer/student-performance/data) y sigue las [instrucciones de la carpeta Datasets](Datasets/README.md). Una vez disponibles, crea un entorno virtual e instala las dependencias de análisis.

**Windows**

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m notebook
```

**macOS y Linux**

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m notebook
```

Ejecuta las celdas de los notebooks en este orden:

1. [Auditoría de los CSV](Notebooks/01_comprension_y_eda.ipynb).
2. [Preparación reproducible](Notebooks/02_preparacion_y_pipeline.ipynb).
3. [Modelado y evaluación](Notebooks/03_modelado_y_validacion.ipynb). La última celda exporta los parámetros a `Prototipo/modelo.json`. Reinicia la demo para cargar esa versión.

La auditoría y el entrenamiento requieren espacio para los archivos originales y memoria para las matrices y controles intermedios. Los notebooks incluyen las salidas de la ejecución de referencia.

## Evidencias

- [Informe editable](Informe_EV3.md).
- [Bitácora y capturas](Imagenes%20Tablero%20Avance%20del%20proyecto/bitacora_tablero.md).
- [Guía de presentación](Guia_presentacion_EV3.md).

Antes de publicar, revisa el contenido de las evidencias y confirma qué datos está autorizado a redistribuir el equipo.
