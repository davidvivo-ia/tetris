# Arquitectura

## Idea

Capas concéntricas con dependencias hacia dentro. El dominio no conoce
nada del mundo: ni Textual, ni ficheros, ni reloj, ni RNG concreto. La
infraestructura provee implementaciones a través de interfaces (Protocol)
definidas en `application/`. La presentación orquesta entrada de usuario
y renderiza estado de dominio.

```
+------------------------------------------------------------+
|                       presentation                         |
|   Textual TUI · CLI Typer · widgets · CSS · bindings       |
+----------------------------|-------------------------------+
                             v
+------------------------------------------------------------+
|                       application                          |
|   Casos de uso: PlaySessionService, ScoreService, Demo     |
|   Protocols: RandomSource, Clock, ScoreRepository          |
+----------------------------|-------------------------------+
                             v
+------------------------------------------------------------+
|                          domain                            |
|   Board · Piece · Tetromino · RotationSystem · Scoring     |
|   GameState (frozen) · GameEvent · pure transitions        |
+------------------------------------------------------------+
                             ^
+----------------------------|-------------------------------+
|                     infrastructure                         |
|   SevenBagRandom · MonotonicClock · JsonScoreRepository    |
+------------------------------------------------------------+
```

Regla de oro: **el flujo de datos entra y sale del dominio; el dominio
nunca llama a las otras capas**.

## Módulos

### `domain/`

Lógica pura. Sin IO, sin tiempo, sin aleatoriedad propia. Modelos
inmutables (`@dataclass(frozen=True, slots=True)`).

- `tetromino.py` — enum `TetrominoKind` con los 7 tipos canónicos.
- `shapes.py` — formas y rotaciones precomputadas como `tuple[tuple[Cell, ...], ...]`.
- `board.py` — `Board` inmutable, `with_locked(piece)`, `cleared()`,
  `is_inside`, `is_blocked`.
- `piece.py` — `Piece` (kind, rotation, x, y) inmutable; `cells()`,
  `moved`, `rotated`.
- `rotation.py` — sistema de kicks (offsets `0, -1, +1, -2, +2`).
- `scoring.py` — función pura `score_for(lines: int, level: int) -> int`
  con tabla BPS escalada (40/100/300/1200).
- `game_state.py` — `GameState` agregado; `EventType` enum y reducer
  `step(state, action) -> tuple[GameState, list[GameEvent]]`.

### `application/`

Orquestación. Define Protocols para todo lo que dependa del exterior.

- `protocols.py` — `RandomSource`, `Clock`, `ScoreRepository`.
- `play_session.py` — `PlaySession`: estado mutable que envuelve
  `GameState` y traduce acciones de presentación a transiciones de
  dominio. Aplica gravedad usando el `Clock`.
- `demo.py` — modo determinista: secuencia de acciones programada con
  seed fija que completa una partida.
- `commands.py` — enum `Action` (MOVE_LEFT, MOVE_RIGHT, SOFT_DROP,
  HARD_DROP, ROTATE_CW, ROTATE_CCW, HOLD, PAUSE, RESET, TICK).

### `infrastructure/`

Implementaciones concretas.

- `random_source.py` — `SevenBagRandom` con seed inyectable.
- `clock.py` — `MonotonicClock` basado en `time.monotonic`.
- `persistence.py` — `JsonScoreRepository` que persiste en
  `$XDG_DATA_HOME/tetris/scores.json` (fallback `~/.local/share/tetris/`).
- `logging.py` — configuración de `structlog`.

### `presentation/`

- `cli.py` — entrada Typer con flags `--seed`, `--demo`, `--level`.
- `tui/app.py` — `TetrisApp`, root de Textual.
- `tui/screens/` — `MenuScreen`, `GameScreen`, `GameOverScreen`.
- `tui/widgets/board.py` — render del tablero con piezas e info.
- `tui/widgets/hud.py` — score, level, lines, next, hold.
- `tui/bindings.py` — mapeo de teclas a `Action`.

### `assets/`

- `tetris.tcss` — estilos Textual.
- `palette.py` — paleta como constantes Python.

## Flujo de un tick

1. Textual emite `on_key` o un `Timer` dispara un tick.
2. `GameScreen` traduce a `Action` y llama `PlaySession.apply(action)`.
3. `PlaySession` llama al reducer `domain.game_state.step`.
4. El reducer devuelve `(GameState', list[GameEvent])`.
5. La presentación reactivamente repinta sólo lo cambiado y, si hay
   eventos (línea limpiada, game over), dispara animaciones / sonido.

## Decisiones rápidas

- **Inmutabilidad estricta en dominio**: cada transición devuelve un
  estado nuevo. Coste despreciable a 10×20.
- **Reducer puro**: facilita tests unitarios y replays.
- **Eventos en vez de callbacks**: el reducer no efectúa side effects;
  emite eventos que la capa de presentación interpreta.
- **Coordenadas**: `x` columna 0..9 (izq→der), `y` fila 0..19
  (arriba→abajo). Las piezas pueden tener `y` negativo brevemente al
  spawn.
- **Spawn**: fila 0, columna 3 (centrado para bbox 4×4).
- **Rotación**: tabla precomputada por compatibilidad con el espíritu
  del original + sistema de kicks tipo SRS simplificado.
