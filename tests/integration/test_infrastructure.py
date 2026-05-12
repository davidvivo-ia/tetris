"""Tests de las implementaciones de infraestructura."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from tetris.application.protocols import Clock, RandomSource, ScoreRepository
from tetris.application.score_entry import ScoreEntry
from tetris.infrastructure.clock import MonotonicClock
from tetris.infrastructure.persistence import MAX_ENTRIES, JsonScoreRepository
from tetris.infrastructure.random_source import SevenBagRandom


def test_seven_bag_is_deterministic_with_seed():
    a = SevenBagRandom(seed=123)
    b = SevenBagRandom(seed=123)
    seq_a = list(a.next_n(14))
    seq_b = list(b.next_n(14))
    assert seq_a == seq_b


def test_seven_bag_contains_each_piece_once_per_seven():
    rng = SevenBagRandom(seed=7)
    first = set(rng.next_n(7))
    second = set(rng.next_n(7))
    assert len(first) == 7
    assert len(second) == 7


def test_seven_bag_default_seed_is_set():
    rng = SevenBagRandom()
    assert rng.seed_used >= 0


def test_seven_bag_satisfies_protocol():
    rng = SevenBagRandom(seed=1)
    assert isinstance(rng, RandomSource)


def test_monotonic_clock_progresses_over_time():
    clock = MonotonicClock()
    assert isinstance(clock, Clock)
    t0 = clock.now()
    t1 = clock.now()
    assert t1 >= t0


def make_entry(score: int) -> ScoreEntry:
    return ScoreEntry(
        name="AAA",
        score=score,
        lines=score // 100,
        level=1 + score // 1000,
        played_at=datetime.now(UTC),
        seed=42,
    )


def test_score_repository_writes_and_reads(tmp_path: Path):
    repo = JsonScoreRepository(path=tmp_path / "scores.json")
    assert isinstance(repo, ScoreRepository)
    assert repo.load() == []
    repo.save(make_entry(500))
    repo.save(make_entry(1500))
    entries = repo.load()
    assert [e.score for e in entries] == [1500, 500]


def test_score_repository_keeps_only_top_n(tmp_path: Path):
    repo = JsonScoreRepository(path=tmp_path / "scores.json")
    for i in range(MAX_ENTRIES + 5):
        repo.save(make_entry(100 * (i + 1)))
    entries = repo.load()
    assert len(entries) == MAX_ENTRIES
    assert entries[0].score >= entries[-1].score
    assert entries[0].score == 100 * (MAX_ENTRIES + 5)


def test_score_repository_handles_corrupt_file(tmp_path: Path):
    path = tmp_path / "scores.json"
    path.write_text("{not valid json")
    repo = JsonScoreRepository(path=path)
    assert repo.load() == []
    saved = repo.save(make_entry(1))
    assert saved[0].score == 1


def test_score_repository_falls_back_to_memory_when_unwritable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    def boom(*_a: object, **_kw: object) -> None:
        raise OSError("read-only filesystem simulado")

    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "touch", boom)
    repo = JsonScoreRepository(path=tmp_path / "blocked.json")
    entries = repo.save(make_entry(7))
    assert entries[0].score == 7
    assert repo.load() == entries
