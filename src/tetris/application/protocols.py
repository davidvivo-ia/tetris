"""Protocols (interfaces) que el dominio/aplicación exigen del exterior."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from tetris.domain.tetromino import TetrominoKind


@runtime_checkable
class RandomSource(Protocol):
    """Proveedor determinista de piezas."""

    def next_kind(self) -> TetrominoKind:
        """Devuelve la siguiente pieza."""
        ...

    def next_n(self, n: int) -> Iterable[TetrominoKind]:
        """Devuelve `n` piezas consecutivas."""
        ...


@runtime_checkable
class Clock(Protocol):
    """Reloj monótono inyectable."""

    def now(self) -> float:
        """Segundos desde un origen arbitrario, monótono creciente."""
        ...


@runtime_checkable
class ScoreRepository(Protocol):
    """Persistencia simple de top-scores."""

    def load(self) -> list[ScoreEntry]:
        """Lee la lista actual de scores (puede estar vacía)."""
        ...

    def save(self, entry: ScoreEntry) -> list[ScoreEntry]:
        """Añade `entry`, persiste y devuelve la lista resultante (top N)."""
        ...


from tetris.application.score_entry import ScoreEntry  # noqa: E402

__all__ = ["Clock", "RandomSource", "ScoreEntry", "ScoreRepository"]
