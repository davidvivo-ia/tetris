#!/usr/bin/env bash
# ======================================================================
#  Tetris 2026 - lanzador para Linux/macOS
#  Prefiere `uv`; cae a venv + pip si no esta disponible.
# ======================================================================
set -euo pipefail

cd "$(dirname "$0")"

if command -v uv >/dev/null 2>&1; then
    exec uv run tetris "$@"
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "No encuentro python3. Instala Python 3.13+ o uv (https://docs.astral.sh/uv/)." >&2
    exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "Creando entorno virtual en .venv ..."
    python3 -m venv .venv
    # shellcheck disable=SC1091
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e .
else
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

exec python -m tetris "$@"
