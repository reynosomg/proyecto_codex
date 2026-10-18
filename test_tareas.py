"""Pruebas del programa completo, con datos temporales."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestTareas(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.archivo = Path(self.carpeta.name) / "tareas.json"

    def ejecutar(self, *argumentos):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("tareas.py")),
             "--archivo", str(self.archivo), *argumentos],
            capture_output=True, text=True,
        )

    def test_ciclo_completo(self):
        self.assertIn("Todavía no hay tareas", self.ejecutar("listar").stdout)
        self.assertEqual(self.ejecutar("agregar", "Aprender Python").returncode, 0)
        self.assertIn("1. [ ] Aprender Python", self.ejecutar("listar").stdout)
        self.assertEqual(self.ejecutar("completar", "1").returncode, 0)
        self.assertIn("1. [x] Aprender Python", self.ejecutar("listar").stdout)

    def test_numero_invalido(self):
        self.assertNotEqual(self.ejecutar("completar", "1").returncode, 0)
        self.assertFalse(self.archivo.exists())

    def test_tarea_vacia(self):
        self.assertNotEqual(self.ejecutar("agregar", "  ").returncode, 0)
        self.assertFalse(self.archivo.exists())

    def test_archivo_invalido_no_se_sobrescribe(self):
        self.archivo.write_text("datos inválidos")
        self.assertNotEqual(self.ejecutar("agregar", "Hola").returncode, 0)
        self.assertEqual(self.archivo.read_text(), "datos inválidos")


if __name__ == "__main__":
    unittest.main()
