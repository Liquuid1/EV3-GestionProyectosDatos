"""Valida un lote CSV y genera resultados con el modelo exportado."""
import argparse
import csv
import json
import math
from pathlib import Path
from tempfile import NamedTemporaryFile

BASE = Path(__file__).resolve().parent


def predecir(fila, modelo):
    curso, horas, extracurricular = (
        float(fila[campo]) for campo in modelo["predictores"]
    )
    if (curso not in (9, 10, 11, 12) or not math.isfinite(horas)
            or horas < 0 or extracurricular not in (0, 1)):
        raise ValueError("Curso, horas de estudio o indicador extracurricular fuera de rango.")
    z = [(valor - media) / escala for valor, media, escala in
         zip((curso, horas, extracurricular), modelo["media"], modelo["escala"])]
    logit = modelo["intercepto"] + sum(x * b for x, b in zip(z, modelo["coeficientes"]))
    probabilidad = 1 / (1 + math.exp(-logit)) if logit >= 0 else math.exp(logit) / (1 + math.exp(logit))
    aportes = {
        campo: (valor - fondo) * coef
        for campo, valor, fondo, coef in zip(
            modelo["predictores"], z, modelo["fondo"], modelo["coeficientes"]
        )
    }
    return dict(probabilidad=probabilidad, alerta=probabilidad >= modelo["umbral"],
                aportes_logit=aportes)


def analizar_lote(archivo, modelo, *, exigir_identidad=False, demo=False):
    lector = csv.DictReader(archivo, strict=True)
    campos = set(lector.fieldnames or [])
    identidad = {"StudentID", "StudentName"}
    requeridos = set(modelo["predictores"])
    if exigir_identidad or campos & identidad:
        requeridos |= identidad
    if not requeridos <= campos or len(campos) != len(lector.fieldnames or []):
        raise ValueError("Columnas requeridas sin duplicados: " + ", ".join(sorted(requeridos)))
    resultados, ids = [], set()
    for numero, fila in enumerate(lector, 1):
        try:
            if None in fila or any(valor is None for valor in fila.values()):
                raise ValueError("El número de campos no coincide con el encabezado.")
            identificador = fila.get("StudentID", f"R{numero:05}").strip()
            nombre = fila.get("StudentName", "").strip()
            if "StudentID" in fila and (not identificador or not nombre or
                                        len(identificador) > 80 or len(nombre) > 160):
                raise ValueError("Indica un ID y nombre válidos.")
            if identificador in ids:
                raise ValueError("StudentID repetido dentro del lote.")
            resultado = predecir(fila, modelo)
        except (ValueError, TypeError) as error:
            raise ValueError(f"Registro {numero}: {error}") from error
        ids.add(identificador)
        resultados.append(dict(id=identificador, nombre=nombre, curso=int(float(fila["Grade"])),
                               **resultado))
    if not resultados:
        raise ValueError("El lote debe tener al menos un registro.")
    return dict(umbral=modelo["umbral"], corte_rendimiento=modelo["corte_rendimiento"],
                registros=resultados, demo_sintetica=demo)


def procesar(entrada, salida, modelo):
    if entrada.resolve() == salida.resolve():
        raise ValueError("La entrada y la salida deben ser archivos distintos.")
    with entrada.open(encoding="utf-8-sig", newline="") as archivo:
        reporte = analizar_lote(archivo, modelo, demo=entrada.resolve() in {
            BASE / "lote_demo.csv", BASE / "lote_demo_b.csv"
        })
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=salida.parent,
                            delete=False) as temporal:
        temporal_path = Path(temporal.name)
        try:
            json.dump(reporte, temporal, indent=2, allow_nan=False)
            temporal.close()
            temporal_path.replace(salida)
        finally:
            temporal_path.unlink(missing_ok=True)
    return reporte


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path)
    parser.add_argument("salida", type=Path)
    args = parser.parse_args()
    try:
        modelo = json.loads((BASE / "modelo.json").read_text())
        reporte = procesar(args.entrada, args.salida, modelo)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Registros procesados: {len(reporte['registros'])}. Salida: {args.salida}")
