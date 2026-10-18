"""Servidor del Prode. Ejecutar con: python app.py."""

import argparse
import json
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

# Nómina base de Primera División 2026. Actualizar al cambiar la temporada.
EQUIPOS = (
    "Aldosivi", "Argentinos Juniors", "Atlético Tucumán", "Banfield",
    "Barracas Central", "Belgrano", "Boca Juniors", "Central Córdoba",
    "Defensa y Justicia", "Deportivo Riestra", "Estudiantes de La Plata",
    "Estudiantes de Río Cuarto", "Gimnasia de La Plata", "Gimnasia de Mendoza",
    "Huracán", "Independiente", "Independiente Rivadavia", "Instituto",
    "Lanús", "Newell’s Old Boys", "Platense", "Racing Club", "River Plate",
    "Rosario Central", "San Lorenzo", "Sarmiento", "Talleres", "Tigre",
    "Unión", "Vélez Sarsfield",
)
STATIC = Path(__file__).parent / "static"


def sortear():
    """Selecciona 16 equipos distintos; su orden define los ocho cruces."""
    return random.sample(EQUIPOS, 16)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ruta = urlsplit(self.path).path
        if ruta == "/api/sorteo":
            contenido = json.dumps({"equipos": sortear()}, ensure_ascii=False).encode()
            tipo = "application/json; charset=utf-8"
        elif ruta in ("/", "/app.js", "/styles.css"):
            archivo = "index.html" if ruta == "/" else ruta[1:]
            contenido = (STATIC / archivo).read_bytes()
            tipo = {"index.html": "text/html", "app.js": "text/javascript",
                    "styles.css": "text/css"}[archivo] + "; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(contenido)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(contenido)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prode de eliminación directa")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    print(f"Prode iniciado en el puerto {args.port}. Ctrl+C para salir.", flush=True)
    try:
        ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
