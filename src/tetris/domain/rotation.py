"""Sistema de kicks al rotar.

Variante simplificada de SRS: prueba la rotación en su lugar, luego con
desplazamientos `(-1, +1, -2, +2)` en `x`. El primer kick que encaja se
acepta; si ninguno encaja, la rotación se rechaza.

[LICENCIA CREATIVA] El original BASIC no aplicaba kicks. Esta
extensión mejora la jugabilidad (B5 del análisis arqueológico).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Final

from tetris.domain.board import Board
from tetris.domain.piece import Piece

KICK_OFFSETS: Final[tuple[int, ...]] = (0, -1, 1, -2, 2)


def try_rotate(
    board: Board, piece: Piece, direction: int, *, kicks: Iterable[int] = KICK_OFFSETS
) -> Piece | None:
    """Intenta rotar la pieza aplicando kicks. Devuelve la pieza nueva o None."""
    rotated = piece.rotated(direction)
    for dx in kicks:
        candidate = rotated.moved(dx, 0)
        if board.fits(candidate):
            return candidate
    return None
