# Build plan

Eight milestones. Each is one issue, one or more commits, and an entry appended
to `PROGRESS.md`.

The benchmark is built early — milestone 3, before consolidation and before
forgetting. Every claim this project makes is a comparative one, so the thing
that produces the comparison cannot be the last thing written.

The inspector is built late — milestone 7, after there is a provenance chain and
a decay curve worth looking at, but before the results writeup, which needs the
figures it produces.

## 1 — Storage layer

- SQLite schema: `episodes`, `facts`, `fact_versions`, `access_log`
- `sqlite-vec` extension loading, with a clear error when it is unavailable
- `MemoryStore` protocol; SQLite implementation
- Migrations, so the schema can change without discarding a store

**Done when:** an episode can be written, retrieved by ID, and vector-searched,
and the store survives a process restart.

## 2 — Embedding and retrieval

- `Embedder` protocol; `SentenceTransformerEmbedder` implementation
- Batched embedding with an on-disk cache keyed by content hash
- Hybrid retrieval: vector similarity blended with recency and access frequency
- Configurable weighting, defaults chosen and then justified in the log

**Done when:** a query returns the planted relevant episode ahead of ten
distractors, and a re-run hits the embedding cache.

## 3 — The benchmark

- Synthetic multi-session conversation generator with planted facts,
  contradictions, and updates
- Ground truth: which fact should be retrieved at which turn
- Scorer: recall accuracy, contradiction resolution, precision, token cost
- Full-context baseline to compare against

**Done when:** the benchmark runs end to end against the milestone-2 system and
produces a number. The number will be mediocre. That is the point — everything
after this is measured against it.

## 4 — Extraction

- `claude-opus-5`, adaptive thinking, structured outputs for fact extraction
- Episode → candidate facts, with confidence and a span reference back to the
  source episode
- Prompt-cache the stable instruction prefix

**Done when:** extraction recovers planted facts from generated conversations at
a measured rate, and that rate is recorded.

## 5 — Consolidation

- Match candidate facts against existing semantic memory
- Classify: new / duplicate / refinement / contradiction
- Supersede on contradiction, preserving the provenance chain
- Idempotence: running consolidation twice must not duplicate or churn facts

**Done when:** benchmark contradiction-resolution accuracy improves measurably
over milestone 3, and consolidation is proven idempotent by test.

## 6 — Forgetting

- Decay scoring from recency, frequency, and age
- Eviction from the retrieval index below threshold, with the row retained
- Measure the effect on both precision and cost

**Done when:** the benchmark shows precision improving as the decay threshold
rises, and the point where recall starts to suffer is identified and documented.

## 7 — The inspector

A read-only web UI over a store file. The point is that the parts of this system
that are hard to argue for in prose — a supersession chain, a decay curve, the
reason one episode outranked another — are easy to argue for on a screen.

- FastAPI read-only JSON API over `MemoryStore`. No endpoint mutates; the
  inspector observes the store, it does not administer it
- React + Vite frontend, served by `recall ui`
- **Facts** — supersession chains rendered as chains: current fact, everything it
  superseded, confidence, and a link back to the source episode span
- **Episodes** — session timeline, full text, and which facts each one produced
- **Retrieval** — a query box that returns ranked results with the score
  decomposed into its vector, recency, and frequency contributions
- **Decay** — decay score over time against the eviction threshold, with evicted
  rows still visible and marked
- **Benchmark** — the recall/cost curve against the full-context baseline, and
  the per-ablation comparison

**Done when:** pointed at the benchmark's store, the inspector shows a planted
contradiction as a supersession chain, and a retrieval's ranking can be explained
from the score decomposition on screen without reading any code.

**Node stays a contributor prerequisite, not a user one.** The built frontend
ships inside the Python package, so `uv sync && recall ui` works on a clone with
no npm install. CI builds it and fails if the committed build is stale.

## 8 — Results and interface

- CLI: `recall ingest`, `recall query`, `recall consolidate`, `recall stats`
- `docs/results.md`: the recall/cost curve against the full-context baseline,
  with the ablations, using figures exported from the inspector
- README quickstart, with inspector screenshots

**Done when:** someone can clone, run the benchmark, and reproduce the headline
number without an API key for the parts that do not require one.
