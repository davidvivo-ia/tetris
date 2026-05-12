@echo off
REM ======================================================================
REM  Tetris 2026 - lanzador para Windows
REM  Doble clic para jugar.
REM
REM  Prefiere `uv` si esta instalado (gestiona Python y deps por ti).
REM  Si no, usa el lanzador `py` con un venv local en .venv\.
REM ======================================================================
setlocal

cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL%==0 (
    uv run tetris %*
    goto :end
)

where py >nul 2>nul
if not %ERRORLEVEL%==0 (
    echo No encuentro Python. Instala Python 3.13+ desde https://www.python.org
    echo o instala uv desde https://docs.astral.sh/uv/.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual en .venv ...
    py -3.13 -m venv .venv || py -3 -m venv .venv
    call ".venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    python -m pip install -e .
) else (
    call ".venv\Scripts\activate.bat"
)

python -m tetris %*

:end
endlocal
