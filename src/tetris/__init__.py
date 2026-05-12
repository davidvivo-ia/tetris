"""Tetris 2026 — reimaginación moderna de un listado BASIC de 1986."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("tetris")
except PackageNotFoundError:  # pragma: no cover - dev install fallback
    __version__ = "1.0.0"

__all__ = ["__version__"]
