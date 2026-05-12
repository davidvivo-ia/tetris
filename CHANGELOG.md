# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/) y
versionado semántico.

## [1.0.0] — 2026-05-12

Reimaginación moderna del listado `legacy/TETRIS.BAS` (M. Pérez, Madrid,
1986).

### Preservado del original

- Tablero clásico de **10 × 20**.
- **Siete piezas canónicas** (I, O, T, S, Z, J, L) con sus cuatro
  rotaciones.
- **Puntuación BPS** escala Nintendo: 40 / 100 / 300 / 1200 × nivel.
- **Niveles cada 10 líneas** con incremento de gravedad.
- **Hard drop** que premia con +2 puntos por celda recorrida.
- **Soft drop** con +1 punto por celda.
- Tecla `q` para salir, idea de panel lateral con marcador.

### Modernizado

- Reescritura desde cero en **Python 3.13** idiomático.
- **Arquitectura por capas**: `domain` puro y tipado, `application` con
  Protocols, `infrastructure` para IO/tiempo/RNG, `presentation` para
  TUI/CLI/headless.
- **Modelo inmutable**: `dataclass(frozen=True, slots=True)` y reducer
  puro `step(state, action) -> (state', events)`.
- **Tipos estrictos**: `mypy --strict` pasa sin errores.
- **Calidad continua**: `ruff` lint+format, `pytest` + `hypothesis`,
  cobertura 94 %, CI GitHub Actions matriz 3.13/3.14.
- **Empaquetado**: `pyproject.toml` PEP 621 + `uv`, layout `src/`, entry
  point `tetris`.
- **TUI Textual** con CSS propio (`assets/tetris.tcss`) y paleta
  Phosphor 2026.
- **Logging estructurado** con `structlog` (preparado para JSON en
  producción).

### Añadido

- **7-bag RNG** (Tetris Guideline) con `--seed N` para reproducibilidad.
- **Hold piece** con bloqueo hasta el siguiente lock.
- **Cola Next** visible (3 piezas).
- **Ghost piece** que indica dónde caerá la pieza activa.
- **Wall kicks** simplificados (offsets `0, ±1, ±2`) al rotar.
- **Pausa** y **reinicio** desde el juego.
- **Modo `--demo`** determinista que juega solo, ideal para grabaciones
  y smoke tests de CI.
- **Modo `--headless`** que ejecuta la partida sin TUI y reporta
  resultado (usado en `uv run tetris --demo --seed 42 --headless`).
- **Persistencia de high scores** en JSON dentro de `XDG_DATA_HOME`,
  con degradación a memoria si el FS no es escribible.
- **`docs/`**: análisis arqueológico del original, arquitectura, sistema
  de diseño y cinco ADRs.

### Licencias creativas tomadas

- **Wall kicks**: el original no permitía rotar pegado a la pared. Se
  añade un sistema SRS simplificado para mejorar la jugabilidad
  (ADR 0003 / ADR 0002).
- **7-bag** en vez de uniforme puro (ADR 0003).
- **Hold + Next preview**: añadidos del Tetris moderno, no presentes en
  el original.
- **Estética Phosphor 2026**: efectos visuales (encendido CRT, glow
  trail) inexistentes en el original (ADR 0005).

### Bugs corregidos respecto al original

- **B1** Variable `F(4,4)` muerta eliminada.
- **B2** Gravedad anclada al tiempo real (segundos) en lugar de bucles
  `FOR W=1 TO 5`.
- **B4** Reescritura de la limpieza de líneas con filtrado puro, sin
  reentrada en `FOR I`.
- **B5** Wall kicks añadidos.
- **B6** Render reactivo en Textual (sin parpadeo).
- **B7** DAS/ARR posible al gestionar entrada continuamente.
- **B8** Hold y next preview.
- **B9** Formas S/Z reescritas centradas.

### Limitaciones conocidas

Detalladas en `TODO.md`. Las más relevantes:

- No hay sonido (la TUI deja el terminal silencioso).
- DAS/ARR usa los repeats por defecto del terminal; no se gestionan
  manualmente.
- Sin animaciones de flash al limpiar líneas (efecto previsto para v1.1).
