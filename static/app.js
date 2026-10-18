"use strict";
const CLAVE = "prode-argentino-v1";
const rondas = ["Octavos de final", "Cuartos de final", "Semifinales", "Final"];
let estado = { equipos: [], elegidos: [[], [], [], []], resultados: [[], [], [], []] };

function participantes(ronda, partido) {
  const fuente = ronda === 0 ? estado.equipos : estado.elegidos[ronda - 1];
  return [fuente[partido * 2], fuente[partido * 2 + 1]];
}

function normalizar() {
  for (let ronda = 0; ronda < 4; ronda++) {
    for (let partido = 0; partido < 8 / (2 ** ronda); partido++) {
      const equipos = participantes(ronda, partido);
      const resultado = estado.resultados[ronda][partido];
      if (resultado) {
        if (!equipos[0] || !equipos[1] ||
            JSON.stringify(resultado.equipos) !== JSON.stringify(equipos)) {
          estado.resultados[ronda][partido] = null;
          estado.elegidos[ronda][partido] = null;
        } else {
          const [a, b] = resultado.goles;
          const valido = v => typeof v === "string" && /^\d{1,2}$/.test(v);
          estado.elegidos[ronda][partido] = valido(a) && valido(b)
            ? (Number(a) === Number(b)
              ? (equipos.includes(resultado.penales) ? resultado.penales : null)
              : equipos[Number(a) > Number(b) ? 0 : 1]) : null;
        }
      } else if (!equipos[0] || !equipos[1] || !equipos.includes(estado.elegidos[ronda][partido])) {
        estado.elegidos[ronda][partido] = null;
      }
    }
  }
}

function actualizar(ronda, partido, resultado) {
  const anterior = estado.elegidos[3][0];
  estado.resultados[ronda][partido] = resultado;
  normalizar(); guardar(); pintar();
  if (estado.elegidos[3][0] !== anterior) {
    document.querySelector("#confeti")?.remove();
    if (estado.elegidos[3][0]) celebrar();
  }
}

let temporizadorConfeti;
function celebrar() {
  document.querySelector("#confeti")?.remove();
  clearTimeout(temporizadorConfeti);
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const capa = document.createElement("div");
  capa.id = "confeti";
  capa.setAttribute("aria-hidden", "true");
  for (let i = 0; i < 110; i++) {
    const papel = document.createElement("i");
    papel.style.left = `${Math.random() * 100}%`;
    papel.style.background = ["#edbd4b", "#ffffff", "#5489e6"][i % 3];
    papel.style.animationDelay = `${Math.random() * .7}s`;
    papel.style.animationDuration = `${2 + Math.random() * 1.5}s`;
    papel.style.setProperty("--giro", `${Math.random() * 1080}deg`);
    capa.append(papel);
  }
  document.body.append(capa);
  temporizadorConfeti = setTimeout(() => capa.remove(), 4500);
}

function guardar() {
  try { localStorage.setItem(CLAVE, JSON.stringify(estado)); }
  catch { document.querySelector("#mensaje").textContent = "No se pudo guardar en este navegador. Podés seguir jugando en esta pestaña."; }
}

function pintar() {
  const cuadro = document.querySelector("#cuadro");
  cuadro.replaceChildren();
  rondas.forEach((nombre, ronda) => {
    const columna = document.createElement("section");
    columna.className = "ronda";
    const titulo = document.createElement("h2");
    titulo.textContent = nombre;
    columna.append(titulo);
    const partidos = document.createElement("div");
    partidos.className = "partidos";
    for (let partido = 0; partido < 8 / (2 ** ronda); partido++) {
      const tarjeta = document.createElement("div");
      tarjeta.className = "partido";
      const equipos = participantes(ronda, partido);
      const activo = Boolean(equipos[0] && equipos[1]);
      const resultado = estado.resultados[ronda][partido];
      const goles = resultado?.goles || ["", ""];
      equipos.forEach((equipo, lado) => {
        const fila = document.createElement("label");
        fila.className = "equipo-marcador";
        const nombre = document.createElement("span");
        const elegido = Boolean(equipo && estado.elegidos[ronda][partido] === equipo);
        fila.classList.toggle("ganador", elegido);
        nombre.textContent = `${elegido ? "✓ " : ""}${equipo || "Por definir"}`;
        const input = document.createElement("input");
        input.type = "number";
        input.min = "0"; input.max = "99"; input.step = "1";
        input.inputMode = "numeric";
        input.placeholder = "–";
        input.value = goles[lado];
        input.disabled = !activo;
        input.setAttribute("aria-label", `Goles de ${equipo || "equipo por definir"}, ${rondas[ronda]}, partido ${partido + 1}`);
        input.addEventListener("change", () => {
          if (input.value !== "" && !/^\d{1,2}$/.test(input.value)) {
            input.setCustomValidity("Ingresá un número entero entre 0 y 99.");
            input.reportValidity();
            return;
          }
          input.setCustomValidity("");
          const nuevos = [...goles]; nuevos[lado] = input.value;
          actualizar(ronda, partido, { equipos: [...equipos], goles: nuevos, penales: null });
        });
        input.addEventListener("input", () => input.setCustomValidity(""));
        fila.append(nombre, input);
        tarjeta.append(fila);
      });
      const empate = activo && goles.every(g => /^\d{1,2}$/.test(g)) && Number(goles[0]) === Number(goles[1]);
      if (empate) {
        const penales = document.createElement("div");
        penales.className = "penales";
        const texto = document.createElement("p");
        texto.textContent = "Empate · ¿Quién gana por penales?";
        penales.append(texto);
        equipos.forEach(equipo => {
          const boton = document.createElement("button");
          boton.textContent = equipo;
          boton.setAttribute("aria-pressed", String(resultado?.penales === equipo));
          boton.addEventListener("click", () => actualizar(ronda, partido,
            { equipos: [...equipos], goles: [...goles], penales: equipo }));
          penales.append(boton);
        });
        tarjeta.append(penales);
      }
      partidos.append(tarjeta);
    }
    columna.append(partidos);
    cuadro.append(columna);
  });
  const total = estado.elegidos.flat().filter(Boolean).length;
  document.querySelector("#progreso").textContent = `${total} de 15 pronósticos`;
  document.querySelector("#campeon h2").textContent = estado.elegidos[3][0] || "La copa espera dueño";
  document.querySelector("#campeon").classList.toggle("completo", Boolean(estado.elegidos[3][0]));
  document.querySelector("#limpiar").disabled = !total && !estado.resultados.flat().some(Boolean);
}

async function sortear(pedirConfirmacion = true) {
  if (pedirConfirmacion && estado.equipos.length && !confirm("¿Sortear otro torneo? Se perderá el cuadro actual.")) return;
  const boton = document.querySelector("#sortear");
  boton.disabled = true;
  document.querySelector("#mensaje").textContent = "Sorteando equipos…";
  try {
    const respuesta = await fetch("/api/sorteo");
    if (!respuesta.ok) throw new Error("sorteo");
    const datos = await respuesta.json();
    if (!Array.isArray(datos.equipos) || datos.equipos.length !== 16 ||
        new Set(datos.equipos).size !== 16 || datos.equipos.some(e => typeof e !== "string" || !e)) throw new Error("equipos");
    document.querySelector("#confeti")?.remove();
    estado = { equipos: datos.equipos, elegidos: [[], [], [], []], resultados: [[], [], [], []] };
    document.querySelector("#mensaje").textContent = "Sorteo listo. Ingresá los goles; si empatan, elegí quién pasa por penales.";
    guardar(); pintar();
  } catch {
    document.querySelector("#mensaje").textContent = "No pudimos sortear los equipos. Comprobá que el servidor siga activo y volvé a intentar.";
  } finally { boton.disabled = false; }
}

document.querySelector("#sortear").addEventListener("click", () => sortear());
document.querySelector("#limpiar").addEventListener("click", () => {
  if (!confirm("¿Borrar tus pronósticos y conservar los mismos cruces?")) return;
  estado.elegidos = [[], [], [], []];
  estado.resultados = [[], [], [], []];
  document.querySelector("#confeti")?.remove();
  guardar(); pintar();
});
try {
  const guardado = JSON.parse(localStorage.getItem(CLAVE));
  if (guardado && Array.isArray(guardado.equipos) && guardado.equipos.length === 16 &&
      new Set(guardado.equipos).size === 16 && guardado.equipos.every(e => typeof e === "string" && e) &&
      Array.isArray(guardado.elegidos) && guardado.elegidos.length === 4 && guardado.elegidos.every(Array.isArray)) {
    estado = { equipos: guardado.equipos, elegidos: guardado.elegidos.map((r, i) => r.slice(0, 8 / (2 ** i))) };
    estado.resultados = [0, 1, 2, 3].map(i =>
      Array.from({ length: 8 / (2 ** i) }, (_, j) => {
        const r = guardado.resultados?.[i]?.[j];
        return r && Array.isArray(r.equipos) && r.equipos.length === 2 &&
          Array.isArray(r.goles) && r.goles.length === 2
          ? { equipos: r.equipos, goles: r.goles, penales: r.penales } : null;
      }));
    normalizar();
  }
} catch { /* Un guardado dañado no impide iniciar un torneo nuevo. */ }
pintar();
if (!estado.equipos.length) sortear(false);
