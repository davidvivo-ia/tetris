"""Modo demo: secuencia determinista que juega sola.

Útil para grabar GIFs, validar regresiones visuales y smoke-tests de CI.
La combinación `(seed=42, secuencia)` es 100 % reproducible.
"""

from __future__ import annotations

from collections.abc import Iterator

from tetris.domain.actions import Action

DEMO_SEED = 42


def demo_actions() -> Iterator[Action]:
    """Genera una secuencia determinista de acciones para una partida demo.

    El plan combina:
        - Algunos hard drops para crecer rápido.
        - Movimientos laterales aleatorios pero predecibles.
        - Rotaciones periódicas.
        - Ticks de gravedad para llenar huecos.

    No pretende jugar bien: pretende ser variada y eventualmente
    terminar en game over para mostrar la pantalla final.
    """
    pattern: tuple[Action, ...] = (
        Action.ROTATE_CW,
        Action.MOVE_LEFT,
        Action.MOVE_LEFT,
        Action.HARD_DROP,
        Action.MOVE_RIGHT,
        Action.ROTATE_CW,
        Action.MOVE_RIGHT,
        Action.MOVE_RIGHT,
        Action.HARD_DROP,
        Action.ROTATE_CCW,
        Action.SOFT_DROP,
        Action.MOVE_LEFT,
        Action.HARD_DROP,
        Action.ROTATE_CW,
        Action.MOVE_RIGHT,
        Action.HARD_DROP,
        Action.HOLD,
        Action.MOVE_RIGHT,
        Action.MOVE_RIGHT,
        Action.HARD_DROP,
    )
    while True:
        yield from pattern
