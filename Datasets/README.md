# Datos para reproducir los notebooks

Descarga el dataset [Student Performance en Kaggle](https://www.kaggle.com/datasets/neuralsorcerer/student-performance/data) y descomprime el archivo descargado. Coloca en esta carpeta los archivos `train.csv`, `validation.csv` y `test.csv` del proyecto EV3. Deben conservar sus nombres y la separación original.

| Archivo | Registros esperados |
|---|---:|
| train.csv | 8.000.774 |
| validation.csv | 999.229 |
| test.csv | 999.997 |

Los tres archivos suman aproximadamente 1,6 GB y se descargan por separado del repositorio. Compara sus sumas SHA-256 con las de [SHA256SUMS](SHA256SUMS) para verificar que coinciden con los archivos usados en EV3. En Linux puedes ejecutar `sha256sum -c SHA256SUMS` desde esta carpeta.

La demostración funciona con el modelo incluido y los lotes sintéticos de `Prototipo/`.
