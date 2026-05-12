"""RNG basado en el sistema 7-bag (Tetris Guideline)."""

from __future__ import annotations

import random
import secrets
from collections.abc import Iterable

from tetris.domain.tetromino import ALL_KINDS, TetrominoKind


class SevenBagRandom:
    """Genera piezas en bolsas de las 7 piezas barajadas.

    Implementa `RandomSource`. Si `seed is None` se obtiene una semilla
    criptográfica accesible vía `seed_used` para que la partida pueda
    reportarse y reproducirse.
    """

    __slots__ = ("_bag", "_rng", "seed_used")

    def __init__(self, seed: int | None = None) -> None:
        """Construye el generador.

        Args:
            seed: semilla determinista. Si es `None`, se genera una
                semilla aleatoria de 63 bits.
        """
        self.seed_used: int = seed if seed is not None else secrets.randbits(63)
        self._rng = random.Random(self.seed_used)
        self._bag: list[TetrominoKind] = []

    def _refill(self) -> None:
        bag = list(ALL_KINDS)
        self._rng.shuffle(bag)
        self._bag.extend(bag)

    def next_kind(self) -> TetrominoKind:
        """Devuelve la siguiente pieza, rellenando la bolsa si es preciso."""
        if not self._bag:
            self._refill()
        return self._bag.pop(0)

    def next_n(self, n: int) -> Iterable[TetrominoKind]:
        """Devuelve `n` piezas consecutivas."""
        return [self.next_kind() for _ in range(n)]
