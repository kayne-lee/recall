"""Extension points.

The `Embedder` boundary is what keeps the benchmark runnable without an API key:
the default implementation is local, and a hosted provider can be dropped in
behind the same protocol when retrieval quality is worth a second credential.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from recall.memory.types import Episode, Fact, Relation


@runtime_checkable
class Embedder(Protocol):
    """Turns text into vectors. Implementations own their own caching."""

    @property
    def dimensions(self) -> int:
        """Vector width. The store's schema depends on this being stable."""
        ...

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch. Order of the output must match order of the input."""
        ...


@runtime_checkable
class MemoryStore(Protocol):
    """Persistence for episodes and facts, plus vector search over both."""

    def add_episode(self, episode: Episode, vector: list[float]) -> None: ...

    def add_fact(self, fact: Fact, vector: list[float]) -> None: ...

    def search_episodes(self, vector: list[float], limit: int) -> list[tuple[Episode, float]]:
        """Nearest episodes with their similarity scores, most similar first."""
        ...

    def search_facts(self, vector: list[float], limit: int) -> list[tuple[Fact, float]]:
        """Nearest *current* facts. Superseded facts are never returned."""
        ...

    def supersede(self, old_fact_id: str, new_fact_id: str) -> None:
        """Mark a fact as replaced, preserving the link in both directions."""
        ...


@runtime_checkable
class Extractor(Protocol):
    """Distils candidate facts out of raw episodes."""

    def extract(self, episodes: list[Episode]) -> list[Fact]: ...


@runtime_checkable
class Consolidator(Protocol):
    """Decides how a candidate fact relates to what is already known.

    Returning CONTRADICTION with a matched fact is the case that matters: it is
    what turns a pile of accumulated claims into a current belief.
    """

    def classify(self, candidate: Fact, existing: list[Fact]) -> tuple[Relation, Fact | None]: ...
