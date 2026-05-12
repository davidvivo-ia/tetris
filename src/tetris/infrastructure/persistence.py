"""Persistencia de high-scores en JSON dentro de XDG_DATA_HOME."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Final

from platformdirs import user_data_dir
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from tetris.application.score_entry import ScoreEntry

APP_NAME = "tetris"
SCHEMA_VERSION: Final[int] = 1
MAX_ENTRIES: Final[int] = 10


class _ScoreFile(BaseModel):
    """Schema de fichero. Validado antes de leerse."""

    model_config = ConfigDict(extra="ignore")

    version: int = Field(ge=1)
    scores: list[ScoreEntry] = Field(default_factory=list)


def default_score_path() -> Path:
    """Ruta canónica del fichero de scores según XDG."""
    base = os.environ.get("XDG_DATA_HOME") or user_data_dir(APP_NAME, appauthor=False)
    return Path(base) / APP_NAME / "scores.json"


class JsonScoreRepository:
    """Repositorio de scores en JSON. Si no puede escribir, degrada a memoria."""

    __slots__ = ("_in_memory", "_path", "_writable")

    def __init__(self, path: Path | None = None) -> None:
        """Construye el repositorio.

        Args:
            path: ruta al fichero. Si `None`, se usa la ruta XDG por defecto.
        """
        self._path = path or default_score_path()
        self._in_memory: list[ScoreEntry] = []
        self._writable: bool = self._probe_writable()

    def _probe_writable(self) -> bool:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch(exist_ok=True)
        except OSError:
            return False
        return True

    def load(self) -> list[ScoreEntry]:
        """Lee los scores actuales o devuelve una lista vacía si no existen."""
        if not self._writable:
            return list(self._in_memory)
        if not self._path.exists() or self._path.stat().st_size == 0:
            return []
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
            parsed = _ScoreFile.model_validate(raw)
        except (json.JSONDecodeError, ValidationError, OSError):
            return []
        return list(parsed.scores)

    def save(self, entry: ScoreEntry) -> list[ScoreEntry]:
        """Añade `entry`, ordena descendentemente y persiste el top N."""
        current = self.load() if self._writable else list(self._in_memory)
        merged = sorted([*current, entry], key=lambda e: e.score, reverse=True)
        top = merged[:MAX_ENTRIES]
        if not self._writable:
            self._in_memory = top
            return top
        payload = _ScoreFile(version=SCHEMA_VERSION, scores=top)
        self._path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")
        return top
