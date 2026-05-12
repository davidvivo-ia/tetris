"""Modelo de entrada de puntuación, usado por el repositorio."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ScoreEntry(BaseModel):
    """Una puntuación persistible."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=12)
    score: int = Field(ge=0)
    lines: int = Field(ge=0)
    level: int = Field(ge=1)
    played_at: datetime
    seed: int | None = None
