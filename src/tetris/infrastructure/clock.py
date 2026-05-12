"""Reloj monótono basado en `time.monotonic`."""

from __future__ import annotations

import time


class MonotonicClock:
    """Implementación trivial de `Clock`."""

    __slots__ = ()

    def now(self) -> float:
        """Segundos monótonos desde un origen arbitrario."""
        return time.monotonic()
