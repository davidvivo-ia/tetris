"""Sesión de juego: une dominio puro con RNG y reloj inyectados."""

from __future__ import annotations

from dataclasses import dataclass, replace

from tetris.application.protocols import Clock, RandomSource
from tetris.domain.actions import Action
from tetris.domain.events import GameEvent
from tetris.domain.game_state import QUEUE_VISIBLE, GameState, new_game, step

INITIAL_QUEUE_SIZE = 7
"""Tamaño inicial de cola tras spawnear la activa."""

_MIN_GRAVITY = 0.05
_BASE_GRAVITY = 0.8
_LEVEL_DECAY = 0.07


def gravity_period(level: int) -> float:
    """Segundos por celda de caída automática al nivel dado."""
    return max(_MIN_GRAVITY, _BASE_GRAVITY - (level - 1) * _LEVEL_DECAY)


@dataclass(slots=True)
class PlaySession:
    """Orquesta el reducer puro con RNG y reloj.

    Mantiene la cola de piezas siempre con al menos `QUEUE_VISIBLE`
    elementos rellenando desde el `RandomSource`. La gravedad la
    dispara `update()` consultando el reloj.
    """

    state: GameState
    _random: RandomSource
    _clock: Clock
    _last_tick: float

    @classmethod
    def start(cls, random: RandomSource, clock: Clock) -> PlaySession:
        """Crea una sesión nueva sembrando la cola con `INITIAL_QUEUE_SIZE` piezas."""
        initial = list(random.next_n(INITIAL_QUEUE_SIZE + 1))
        state = new_game(initial)
        return cls(state=state, _random=random, _clock=clock, _last_tick=clock.now())

    def apply(self, action: Action) -> tuple[GameState, tuple[GameEvent, ...]]:
        """Aplica una acción del usuario y refresca la cola si hace falta."""
        new_state, events = step(self.state, action)
        new_state = self._refill_queue(new_state)
        if action is Action.TICK:
            self._last_tick = self._clock.now()
        self.state = new_state
        return new_state, events

    def update(self) -> tuple[GameState, tuple[GameEvent, ...]]:
        """Si toca, aplica un TICK por gravedad. En caso contrario, no hace nada."""
        if self.state.game_over or self.state.paused:
            self._last_tick = self._clock.now()
            return self.state, ()
        elapsed = self._clock.now() - self._last_tick
        if elapsed < gravity_period(self.state.level):
            return self.state, ()
        return self.apply(Action.TICK)

    def reset(self) -> GameState:
        """Reinicia la partida con piezas frescas del RNG."""
        initial = list(self._random.next_n(INITIAL_QUEUE_SIZE + 1))
        self.state = new_game(initial)
        self._last_tick = self._clock.now()
        return self.state

    def _refill_queue(self, state: GameState) -> GameState:
        if len(state.queue) >= QUEUE_VISIBLE:
            return state
        missing = QUEUE_VISIBLE - len(state.queue)
        extra = tuple(self._random.next_n(missing))
        return replace(state, queue=state.queue + extra)
