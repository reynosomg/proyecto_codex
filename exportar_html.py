"""Genera prode.html para abrir o compartir sin ejecutar el servidor."""

import json
from pathlib import Path

from app import EQUIPOS

BASE = Path(__file__).parent


def exportar(destino=None):
    html = (BASE / "static/index.html").read_text(encoding="utf-8")
    css = (BASE / "static/styles.css").read_text(encoding="utf-8")
    javascript = (BASE / "static/app.js").read_text(encoding="utf-8")
    # La versión portable usa la misma nómina y lógica del cuadro.
    javascript = javascript.replace(
        'const respuesta = await fetch("/api/sorteo");',
        'const respuesta = await sorteoLocal();',
    ).replace(
        "Comprobá que el servidor siga activo y volvé a intentar.",
        "Volvé a intentar.",
    )
    local = """
function sorteoLocal() {
  const equipos = [...NOMINA];
  for (let i = equipos.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [equipos[i], equipos[j]] = [equipos[j], equipos[i]];
  }
  return { ok: true, json: async () => ({ equipos: equipos.slice(0, 16) }) };
}
"""
    javascript = "const NOMINA = " + json.dumps(EQUIPOS, ensure_ascii=False) + ";\n" + local + javascript
    html = html.replace('<link rel="stylesheet" href="/styles.css">', f"<style>\n{css}\n</style>")
    html = html.replace('<script src="/app.js" defer></script>', "")
    html = html.replace('href="/"', 'href="#"')
    html = html.replace("</body>", f"<script>\n{javascript}\n</script>\n</body>")
    destino = Path(destino) if destino else BASE / "prode.html"
    destino.write_text(html, encoding="utf-8")
    return destino


if __name__ == "__main__":
    print(exportar())
