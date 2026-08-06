from datetime import UTC, datetime

import pytest

from recall.memory.types import Episode, Fact


def make_episode(**overrides: object) -> Episode:
    defaults = {
        "session_id": "s1",
        "content": "The project is written in Rust.",
        "timestamp": datetime(2026, 3, 4, tzinfo=UTC),
    }
    return Episode(**{**defaults, **overrides})  # type: ignore[arg-type]


def test_episode_id_is_derived_and_stable() -> None:
    assert make_episode().episode_id == make_episode().episode_id


def test_episode_id_varies_with_content() -> None:
    a = make_episode()
    b = make_episode(content="The project is written in Go.")
    assert a.episode_id != b.episode_id


def test_episode_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        make_episode(content="   ")


def test_episode_requires_aware_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        make_episode(timestamp=datetime(2026, 3, 4))


def test_fact_currency_tracks_supersession() -> None:
    fact = Fact(content="Lives in Kingston", fact_id="f1")
    assert fact.is_current
    fact.superseded_by = "f2"
    assert not fact.is_current


def test_fact_rejects_out_of_range_confidence() -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        Fact(content="x", fact_id="f1", confidence=1.5)
