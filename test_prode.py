import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen
from http.server import ThreadingHTTPServer

from app import EQUIPOS, Handler, sortear


class TestProde(unittest.TestCase):
    def test_sorteo_sin_repetidos(self):
        self.assertEqual(len(EQUIPOS), len(set(EQUIPOS)))
        for _ in range(20):
            equipos = sortear()
            self.assertEqual(len(equipos), 16)
            self.assertEqual(len(set(equipos)), 16)
            self.assertTrue(set(equipos) <= set(EQUIPOS))

    def test_servidor_y_sorteo(self):
        servidor = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
        hilo.start()
        try:
            base = f"http://127.0.0.1:{servidor.server_port}"
            with urlopen(base + "/api/sorteo", timeout=5) as respuesta:
                self.assertEqual(len(set(json.load(respuesta)["equipos"])), 16)
            for ruta, contenido in [("/", b"cuadro"), ("/app.js", b"normalizar"),
                                    ("/styles.css", b"@media")]:
                with urlopen(base + ruta, timeout=5) as respuesta:
                    self.assertIn(contenido, respuesta.read())
            with self.assertRaises(HTTPError) as error:
                urlopen(base + "/app.py", timeout=5)
            self.assertEqual(error.exception.code, 404)
        finally:
            servidor.shutdown()
            servidor.server_close()
            hilo.join()


if __name__ == "__main__":
    unittest.main()
