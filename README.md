# Prode · Camino a la copa

App web en Python para pronosticar un torneo de fantasía con equipos del fútbol argentino.

## Abrir sin servidor

Abrí `prode.html` en un navegador. Incluye estilos, lógica y sorteo en un único archivo, sin conexiones de red. También podés compartir ese archivo. El guardado depende de que el navegador permita almacenamiento local; si está bloqueado, podés jugar durante la sesión.

Para regenerarlo después de editar la app:

```bash
python exportar_html.py
```

El visor de archivos sueltos no puede cargar los recursos de `static/index.html` ni ejecutar la API de Python. Usá `prode.html` en ese caso. Algunos visores restringen JavaScript: si ocurre, descargá el archivo y abrilo en tu navegador.

## Ejecutar

Requiere Python 3.10 o superior. No necesita instalar paquetes.

```bash
cd /workspace/proyecto_codex
python app.py
```

En tu computadora, abrí `http://localhost:8000`. Ctrl+C detiene el servidor. Para elegir otro puerto: `python app.py --port 8080`.

## Cómo jugar

1. Se sortean 16 equipos distintos para los octavos.
2. Ingresá los goles de cada equipo (de 0 a 99). Si hay empate, elegí quién pasa por penales. Al definir al campeón aparece confeti.
3. Si cambiás un ganador, se limpian los pronósticos posteriores que dependían de él.

**Reiniciar pronóstico** conserva los cruces. **Sortear equipos** crea otro torneo. Ambas acciones piden confirmación.

El cuadro se guarda en tu navegador. Esta versión no tiene cuentas, puntajes, resultados reales ni sincronización entre dispositivos. Los marcadores determinan quién clasifica; en los empates elegís al ganador por penales. El confeti respeta la preferencia de reducir movimiento.

La nómina base para 2026 está en `EQUIPOS` dentro de `app.py`. Es una lista local de 30 equipos, sin actualización automática desde una fuente oficial; revisala al cambiar de temporada.

## Pruebas

```bash
python -m unittest -v
```

## Archivos

- `app.py`: servidor y sorteo.
- `static/index.html`: pantalla.
- `static/styles.css`: diseño adaptable a celular.
- `static/app.js`: cuadro, pronósticos y guardado.
- `test_prode.py`: pruebas del sorteo y servidor.

También se conserva el ejemplo inicial `tareas.py` con sus pruebas. El servidor es para desarrollo.

El diseño usa azul marino, dorado y blanco, inspirado en la LPF. Los títulos usan fuentes condensadas del sistema como alternativa a la tipografía oficial; no incluye fuentes ni escudos oficiales.
