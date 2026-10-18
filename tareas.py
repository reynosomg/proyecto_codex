"""Una pequeña lista de tareas para practicar Python y Codex."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Tu lista de tareas")
    parser.add_argument("--archivo", type=Path, default=Path("tareas.json"))
    comandos = parser.add_subparsers(dest="comando", required=True)
    agregar = comandos.add_parser("agregar", help="Agrega una tarea")
    agregar.add_argument("texto")
    comandos.add_parser("listar", help="Muestra las tareas")
    completar = comandos.add_parser("completar", help="Marca una tarea como hecha")
    completar.add_argument("numero", type=int)
    args = parser.parse_args()

    try:
        tareas = json.loads(args.archivo.read_text()) if args.archivo.exists() else []
        if not isinstance(tareas, list) or any(
            not isinstance(t, dict)
            or not isinstance(t.get("texto"), str)
            or not isinstance(t.get("hecha"), bool)
            for t in tareas
        ):
            raise ValueError("El archivo no contiene una lista de tareas válida")
        if args.comando == "listar":
            if not tareas:
                print("Todavía no hay tareas.")
            for numero, tarea in enumerate(tareas, start=1):
                marca = "x" if tarea["hecha"] else " "
                print(f"{numero}. [{marca}] {tarea['texto']}")
            return
        if args.comando == "agregar":
            texto = args.texto.strip()
            if not texto:
                parser.error("La tarea no puede estar vacía")
            tareas.append({"texto": texto, "hecha": False})
        else:
            if not 1 <= args.numero <= len(tareas):
                parser.error("Ese número de tarea no existe")
            tareas[args.numero - 1]["hecha"] = True
        args.archivo.write_text(json.dumps(tareas, ensure_ascii=False, indent=2) + "\n")
        print("Lista guardada.")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
