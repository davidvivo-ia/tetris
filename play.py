#!/usr/bin/env python3
"""Lanzador directo del juego: `python play.py [opciones]`.

No requiere instalar el paquete: añade `src/` al `sys.path` y delega
al CLI Typer. Las dependencias (textual, typer, rich, pydantic,
structlog, platformdirs) tienen que estar instaladas en el intérprete
con el que ejecutes este script.

Si no las tienes, la forma más rápida es:

    pip install -e .

O, si prefieres `uv`:

    uv sync && uv run tetris

Ejemplos:

    python play.py
    python play.py --seed 1986
    python play.py --demo --seed 42
    python play.py --demo --seed 42 --headless --max-ticks 200
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    src = Path(__file__).resolve().parent / "src"
    src_str = str(src)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)


def main() -> None:
    _ensure_src_on_path()
    try:
        from tetris.presentation.cli import app
    except ModuleNotFoundError as exc:
        missing = exc.name or "una dependencia"
        sys.stderr.write(
            f"Falta la dependencia '{missing}'.\n"
            "Instala las deps con una de estas opciones:\n"
            "  pip install -e .\n"
            "  uv sync && uv run tetris\n"
        )
        sys.exit(1)
    app()


if __name__ == "__main__":
    main()
