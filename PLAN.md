# Build plan

Seven milestones. Each is one issue, one or more commits, and an entry appended
to `PROGRESS.md`.

The benchmark is built early — milestone 3, before consolidation and before
forgetting. Every claim this project makes is a comparative one, so the thing
that produces the comparison cannot be the last thing written.

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

## 7 — Results and interface

- CLI: `recall ingest`, `recall query`, `recall consolidate`, `recall stats`
- `docs/results.md`: the recall/cost curve against the full-context baseline,
  with the ablations
- README quickstart

**Done when:** someone can clone, run the benchmark, and reproduce the headline
number without an API key for the parts that do not require one.
