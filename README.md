# Tetris 2026

Reimaginación moderna de un listado **Tetris en BASIC de 1986** (ver
`legacy/TETRIS.BAS`). Misma alma — siete piezas, gravedad, líneas,
puntuación BPS — otra época: dominio puro tipado estricto, TUI Textual
con la estética **Phosphor 2026**, modo demo determinista y empaquetado
moderno (`uv`, `pyproject.toml`, CI).

```
┌────────────────────────┐  ┌─────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░ │  │ SCORE     12350 │
│ ░░░░░░██░░░░░░░░░░░░░░ │  │ LINES        42 │
│ ░░░░░░██░░░░░░░░░░░░░░ │  │ LEVEL         5 │
│ ░░░░██████░░░░░░░░░░░░ │  ├─────────────────┤
│ ░░░░░░░░░░░░░░░░░░░░░░ │  │ NEXT            │
│ ░░░░░░░░░░░░░░░░░░░░░░ │  │   ████          │
│ ░░░░░░░░░░░░░░░░░░░░░░ │  │   ██  ██        │
│ ░░░░░░░░░░░░░░░░░░░░░░ │  │       ████      │
│ ░░░░░░░░▒▒▒▒▒▒░░░░░░░░ │  ├─────────────────┤
│ ░░░░░░░░░░░░░░░░░░░░░░ │  │ HOLD            │
│ ░░██░░░░░░░░░░░░░░░░██ │  │   ████          │
│ ░░████████████░░░░░░██ │  ├─────────────────┤
│ ████████████████████░░ │  │ ←/→  mover      │
└────────────────────────┘  │ ↑/x  rotar      │
                            │ esp  hard drop  │
                            │ c    hold       │
                            └─────────────────┘
```

## Inicio rápido

```bash
# instalar dependencias en un entorno virtual administrado por uv
uv sync

# jugar (Textual; necesita un terminal con soporte de teclas y color)
uv run tetris

# partida con semilla reproducible
uv run tetris --seed 1986

# demo determinista (juega sola)
uv run tetris --demo --seed 42

# smoke test headless (CI)
uv run tetris --demo --seed 42 --headless --max-ticks 200
```

Requiere **Python 3.13+**. `uv` se encarga del intérprete y las deps.

## Controles

| Tecla         | Acción                                    |
|---------------|-------------------------------------------|
| `←` / `→`     | Mover lateralmente                        |
| `↓`           | Soft drop (+1 punto por celda)            |
| `↑` o `x`     | Rotar (horario)                           |
| `z`           | Rotar (antihorario)                       |
| `Espacio`     | Hard drop (+2 puntos por celda)           |
| `c`           | Hold (intercambiar)                       |
| `p`           | Pausa                                     |
| `r`           | Reiniciar                                 |
| `q`           | Salir                                     |

## Estructura

```
.
├── legacy/                # TETRIS.BAS (1986) — read-only
├── docs/                  # arquitectura, diseño, ADRs, postmortem
├── src/tetris/
│   ├── domain/            # núcleo puro: Board, Piece, GameState, reducer
│   ├── application/       # casos de uso, protocols, demo
│   ├── infrastructure/    # RNG 7-bag, reloj, persistencia JSON+XDG
│   ├── presentation/      # CLI Typer + TUI Textual + headless
│   └── assets/            # paleta y tetris.tcss
└── tests/                 # unit, integration, property (hypothesis)
```

Lectura recomendada: `docs/architecture.md`, `docs/design.md` y los
ADRs en `docs/adr/`.

## Calidad

| Gate               | Estado |
|--------------------|--------|
| `ruff format`      | limpio |
| `ruff check`       | limpio |
| `mypy --strict`    | sin errores |
| `pytest`           | 91 tests verdes |
| Cobertura `domain` | 95%    |
| Cobertura total    | 94%    |

CI en GitHub Actions corre la matriz Python 3.13 / 3.14.

## Decisiones clave

- **Dominio inmutable y puro** (`dataclass(frozen=True, slots=True)`); el
  reducer `step(state, action) -> (state', events)` no tiene IO ni RNG.
- **RNG inyectado** con 7-bag (Tetris Guideline) y `--seed N` para
  partidas reproducibles.
- **Rotación con kicks** simplificados (offsets `0, ±1, ±2`) — el
  original no los tenía.
- **Persistencia ligera** en `${XDG_DATA_HOME}/tetris/scores.json`, con
  degradación silenciosa a memoria si el FS es de sólo lectura.

Trade-offs y limitaciones documentadas en `TODO.md` para v1.1.

## Filosofía

El listado original cabía en 200 líneas de BASIC tecleadas a mano desde
una revista. Esta versión renueva todo lo que el oficio ha aprendido en
40 años (capas, tipos, pruebas, accesibilidad) preservando el alma del
juego. El detalle en `docs/postmortem.md`.

## Licencia

MIT. Ver `LICENSE`.
