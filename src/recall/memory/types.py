"""Memory value types.

The distinction that matters here is between an Episode and a Fact.

An Episode is a record of something that happened at a time. It is append-only
and never edited — a log entry that turns out to be wrong is still an accurate
record of what was said.

A Fact is a claim believed to be currently true, distilled from one or more
episodes. Facts are superseded rather than mutated, so the chain from a current
belief back through every belief it replaced stays intact.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class Relation(Enum):
    """How a candidate fact relates to what is already stored."""

    NEW = "new"
    DUPLICATE = "duplicate"
    REFINEMENT = "refinement"
    CONTRADICTION = "contradiction"


@dataclass(frozen=True, slots=True)
class Episode:
    """Something that happened, at a time. Append-only."""

    session_id: str
    content: str
    timestamp: datetime
    speaker: str = "user"
    episode_id: str = ""

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("episode content cannot be empty")
        if self.timestamp.tzinfo is None:
            raise ValueError("episode timestamp must be timezone-aware")
        if not self.episode_id:
            digest = hashlib.sha256(
                f"{self.session_id}\x00{self.timestamp.isoformat()}\x00{self.content}".encode()
            ).hexdigest()[:16]
            object.__setattr__(self, "episode_id", digest)


@dataclass(slots=True)
class Fact:
    """A claim believed currently true, distilled from episodes.

    `superseded_by` being set means this fact is history: it is retained for
    provenance but must never be returned by retrieval.
    """

    content: str
    fact_id: str
    source_episode_ids: list[str] = field(default_factory=list)
    confidence: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    superseded_by: str | None = None
    supersedes: str | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0, 1], got {self.confidence}")

    @property
    def is_current(self) -> bool:
        return self.superseded_by is None


@dataclass(slots=True)
class DecayState:
    """Inputs to the forgetting score for a single memory.

    Kept separate from Episode and Fact deliberately: access statistics change
    constantly and those two types are meant to be stable.
    """

    memory_id: str
    access_count: int = 0
    last_accessed: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
