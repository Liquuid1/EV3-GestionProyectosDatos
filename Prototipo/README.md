# Demostración local de EV3

Desde la raíz del proyecto, ejecuta con Python 3:

```bash
python3 Prototipo/dashboard.py
```

El servidor pide una contraseña para el usuario `demo`. Abre http://127.0.0.1:8765/ e ingresa esas credenciales. El panel comienza vacío. Carga un CSV válido para ver el resumen y seleccionar a un estudiante. Para volver a exportar el modelo, ejecuta el notebook 03 en el entorno de entrenamiento.

El prototipo se sirve exclusivamente en la dirección local y protege la consulta con un usuario de demostración. El despliegue institucional, los roles diferenciados y el cifrado de transporte quedan pendientes.

## Carga en el navegador y trazabilidad

Usa **Cargar lote de estudiantes** y selecciona `lote_demo.csv` (dos alertas) o `lote_demo_b.csv` (una alerta). Cada carga válida reemplaza el lote visible sin reiniciar. Las cargas de navegador se mantienen en memoria durante la sesión del servidor.

El CSV del navegador requiere `StudentID,StudentName,Grade,StudyHours,Extracurricular`. El encargado exporta el código interno y el nombre del alumno desde el registro institucional y agrega sus predictores. Debe conservar el mismo código entre cargas. El panel muestra nombre, código y curso en el listado y en la ficha. La inferencia usa únicamente los tres predictores. El prototipo permite identificar a cada estudiante en el lote vigente. Un historial por fecha y permisos diferenciados para carga y consulta quedan como trabajo del piloto. Para la presentación usa los archivos sintéticos.
