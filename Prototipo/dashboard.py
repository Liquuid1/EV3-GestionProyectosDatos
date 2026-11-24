"""Panel de demostración con autenticación HTTP y acceso local."""
import argparse
import base64
from getpass import getpass
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import csv
from io import StringIO
from secrets import compare_digest, token_urlsafe
from inferencia import BASE, analizar_lote
from urllib.parse import parse_qs, urlencode, urlsplit

NOMBRES = {"Grade": "Curso", "StudyHours": "Horas de estudio",
           "Extracurricular": "Participación extracurricular"}


def porcentaje(valor):
    return f"{valor:.2%}".replace(".", ",")


def renderizar_resultados(reporte, seleccionado):
    if reporte is None:
        return ""
    registros = reporte["registros"]
    alertas = sum(r["alerta"] for r in registros)
    detalle = next((r for r in registros if r["id"] == seleccionado), None)
    tasa = alertas / len(registros)
    filas = []
    for registro in sorted(registros, key=lambda r: r["probabilidad"], reverse=True)[:12]:
        identificador = escape(registro["id"])
        nombre = escape(registro.get("nombre") or registro["id"])
        curso = registro.get("curso", "—")
        vinculo = urlencode({"registro": registro["id"]})
        estado = "Revisar" if registro["alerta"] else "Sin alerta"
        clase = "alerta" if registro["alerta"] else "normal"
        actual = ' aria-current="true"' if registro is detalle else ""
        filas.append(f"""
        <tr><td><a href="?{vinculo}#detalle"{actual}>{nombre}</a><br><small>{identificador} · Curso {curso}</small></td>
        <td>{porcentaje(registro['probabilidad'])}</td>
        <td><span class="estado {clase}">{estado}</span></td></tr>""")
    tabla = "".join(filas)
    caso = '<p>Selecciona un registro de la lista o consulta por identificador.</p>'
    if detalle:
        estado = "Revisión sugerida" if detalle["alerta"] else "Sin alerta"
        clase = "alerta" if detalle["alerta"] else "normal"
        aportes = []
        for clave, valor in sorted(detalle["aportes_logit"].items(),
                                   key=lambda par: abs(par[1]), reverse=True):
            nombre = escape(NOMBRES.get(clave, clave))
            magnitud = f"{valor:+.4f}".replace(".", ",")
            if abs(valor) < 0.00005:
                magnitud = "≈ 0"
            aportes.append(f"<li><span>{nombre}</span><strong>{magnitud}</strong></li>")
        caso = f"""<div class="caso"><strong>{escape(detalle.get('nombre') or detalle['id'])}</strong>
        <span class="estado {clase}">{estado}</span></div>
        <p class="suave">{escape(detalle['id'])} · Curso {detalle.get('curso', '—')}</p>
        <p class="riesgo">{porcentaje(detalle['probabilidad'])}</p>
        <p class="suave">Probabilidad estimada de bajo rendimiento relativo</p>
        <h3>Aportes por variable</h3><ul class="aportes">{''.join(aportes)}</ul>
        <p class="suave">Los valores positivos aumentan la estimación y los negativos la reducen.
        Se expresan en la escala del modelo, no en puntos porcentuales.</p>"""
    busqueda = escape(seleccionado, quote=True)
    return f"""<dl aria-label="Resumen del lote">
<div><dt>Registros analizados</dt><dd>{len(registros)}</dd></div>
<div><dt>Alertas para revisión</dt><dd>{alertas}</dd></div>
<div><dt>Tasa de alertas</dt><dd>{porcentaje(tasa)}</dd></div>
<div><dt>Umbral de alerta</dt><dd>{porcentaje(reporte['umbral'])}</dd></div>
</dl>
<div class="contenido">
<section><h2>Registros por probabilidad</h2>
<p class="suave">Mostrando {len(filas)} de {len(registros)}. Selecciona un identificador para ver su detalle.</p>
<table><thead><tr><th>Estudiante</th><th>Probabilidad</th><th>Estado</th></tr></thead>
<tbody>{tabla}</tbody></table></section>
<section id="detalle"><h2>Detalle del registro</h2>
<form action="/#detalle" method="get"><label for="registro">Identificador</label>
<input id="registro" name="registro" value="{busqueda}" required><button>Consultar</button></form>
{caso}</section></div>
<footer class="suave">Las alertas orientan la revisión pedagógica y requieren confirmación humana.</footer>
"""


def renderizar(reporte, seleccionado, token=""):
    origen = "Lote sintético de demostración" if reporte and reporte.get("demo_sintetica") else "Lote procesado" if reporte else "Sin lote cargado"
    return f"""<!doctype html>
<html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seguimiento académico · EV3</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f1f5f8;color:#152b40;font:16px/1.5 system-ui,sans-serif}}
main{{max-width:1160px;margin:auto;padding:28px clamp(14px,4vw,42px)}}
header{{background:linear-gradient(115deg,#142c48,#18585e);color:white;padding:clamp(22px,5vw,44px);border-radius:22px}}
header p{{margin:0;color:#d0ecea}}h1{{margin:.25rem 0 0;font-size:clamp(1.8rem,4vw,3rem);line-height:1.12}}
h2{{font-size:1.22rem;margin:0 0 14px}}h3{{font-size:1rem;margin:20px 0 6px}}
dl{{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:12px;margin:16px 0}}
dl div,section{{background:white;border:1px solid #dbe5ec;border-radius:16px;padding:18px}}
dt,.suave{{color:#496176}}dd{{font-size:1.85rem;font-weight:750;margin:0}}
.contenido{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:16px}}
table{{width:100%;border-collapse:collapse;text-align:left}}th,td{{padding:9px 5px;border-bottom:1px solid #e7edf2}}
th{{font-size:.82rem;color:#496176}}tr:has([aria-current]){{background:#edf7f6}}
a{{color:#075b62;font-weight:700}}:focus-visible{{outline:3px solid #14767d;outline-offset:3px}}
.estado{{display:inline-block;padding:3px 8px;border-radius:99px;font-size:.79rem;font-weight:700}}
.alerta{{background:#fff0d4;color:#7d4200}}.normal{{background:#e7f4ef;color:#175b45}}
form,.caso{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}.caso{{margin-top:16px}}
label{{width:100%;font-size:.85rem}}input,button{{font:inherit;padding:7px 10px;border-radius:8px}}
input{{width:9em;max-width:100%;border:1px solid #a8bac7}}button{{background:#125b63;color:white;border:0;cursor:pointer}}
.riesgo{{font-size:2rem;font-weight:750;margin:3px 0}}.suave{{font-size:.88rem;margin:3px 0}}
.aportes{{list-style:none;padding:0;margin:0 0 10px}}.aportes li{{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid #e7edf2;padding:6px 0}}
footer{{margin-top:14px}}@media(max-width:720px){{.contenido{{grid-template-columns:1fr}}}}
</style>
<main><header><p>{origen}</p><h1>Seguimiento académico en Matemáticas</h1></header>
<section style="margin-top:16px"><h2>Cargar lote de estudiantes</h2>
<form id="carga"><label for="csv">Archivo CSV con ID, nombre, curso, horas de estudio y participación extracurricular</label>
<input style="width:auto" id="csv" type="file" accept=".csv,text/csv" required>
<button>Procesar lote</button></form>
<p role="status" id="estado-carga"></p>
</section>
<script>
document.getElementById('carga').addEventListener('submit', async event => {{
    event.preventDefault();
    const archivo = document.getElementById('csv').files[0];
    const estado = document.getElementById('estado-carga');
    const boton = event.currentTarget.querySelector('button');
    boton.disabled = true;
    estado.textContent = 'Procesando lote…';
    try {{
        const respuesta = await fetch('/lote', {{
            method: 'POST', headers: {{'Content-Type': 'text/csv', 'X-Lote-Token': '{token}'}},
            body: archivo
        }});
        if (respuesta.ok) window.location.assign('/');
        else estado.textContent = await respuesta.text();
    }} catch {{
        estado.textContent = 'No se pudo completar la carga. Intenta nuevamente.';
    }} finally {{
        boton.disabled = false;
    }}
}});
</script>
{renderizar_resultados(reporte, seleccionado)}
</main></html>"""


def crear_handler(contrasena):
    reporte = None
    token = base64.b64encode(f"demo:{contrasena}".encode()).decode()
    autorizado = f"Basic {token}".encode()

    token_carga = token_urlsafe(24)
    modelo = json.loads((BASE / "modelo.json").read_text())
    demos = {(BASE / nombre).read_bytes() for nombre in ("lote_demo.csv", "lote_demo_b.csv")}

    class Dashboard(BaseHTTPRequestHandler):
        def autenticar(self):
            recibido = self.headers.get("Authorization", "").encode()
            if not compare_digest(recibido, autorizado):
                self.send_response(401)
                self.send_header("WWW-Authenticate", 'Basic realm="EV3"')
                self.end_headers()
                return False
            return True

        def do_GET(self):
            if not self.autenticar():
                return
            url = urlsplit(self.path)
            if url.path != "/":
                self.send_error(404)
                return
            actual = reporte
            primero = actual["registros"][0]["id"] if actual else ""
            elegido = parse_qs(url.query).get("registro", [primero])[0]
            contenido = renderizar(actual, elegido, token_carga).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(contenido)))
            self.end_headers()
            self.wfile.write(contenido)

        def do_POST(self):
            nonlocal reporte
            if not self.autenticar():
                return
            if self.path != "/lote":
                self.send_error(404)
                return
            if not compare_digest(self.headers.get("X-Lote-Token", "").encode(), token_carga.encode()):
                self.send_error(403)
                return
            try:
                longitud = int(self.headers.get("Content-Length", "0"))
                if not 0 < longitud <= 2 * 1024 * 1024:
                    raise ValueError("Selecciona un CSV de hasta 2 MiB.")
                datos = self.rfile.read(longitud)
                nuevo = analizar_lote(StringIO(datos.decode("utf-8-sig"), newline=""),
                                      modelo, exigir_identidad=True, demo=datos in demos)
            except (ValueError, csv.Error) as error:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(f"No se cambió el lote. {error}".encode())
                return
            reporte = nuevo
            self.send_response(204)
            self.end_headers()

    return Dashboard


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--puerto", type=int, default=8765)
    args = parser.parse_args()
    contrasena = getpass("Contraseña para el usuario demo: ")
    if not contrasena:
        parser.error("La contraseña de demostración es obligatoria.")
    with ThreadingHTTPServer(("127.0.0.1", args.puerto), crear_handler(contrasena)) as servidor:
        print(f"Dashboard en http://127.0.0.1:{args.puerto}/")
        servidor.serve_forever()
