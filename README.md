# recall

A memory system for LLM agents: episodic and semantic stores with consolidation,
decay-based forgetting, and a benchmark that measures whether any of it helps.

## The problem

The default way to give an agent memory is to append everything to the context
window. This works until it doesn't. Cost grows linearly with conversation
length, retrieval accuracy degrades as the relevant fact gets buried among
thousands of irrelevant ones, and nothing ever resolves the moment the user says
"actually, I moved to Toronto" three sessions after saying they lived in Kingston.

`recall` treats memory as something that is written, consolidated, retrieved, and
eventually forgotten — and measures each of those against a naive baseline.

## Memory types

**Working** — the current session's scratch space. Cheap, complete, discarded or
promoted when the session ends.

**Episodic** — timestamped records of what happened. "On 2026-03-04 the user said
they were switching the project to Rust." Retrieved by a blend of semantic
similarity and recency. Episodic memory is append-only; it is a log, and logs are
not edited.

**Semantic** — durable facts distilled from episodes. "The project is written in
Rust." Deduplicated on write and versioned, so a contradiction supersedes rather
than coexists with what it contradicts.

## Consolidation

The interesting part. A consolidation pass reads recent episodes and:

1. Extracts candidate facts
2. Matches each against existing semantic memory
3. Classifies the relationship — new, duplicate, refinement, or **contradiction**
4. On contradiction, supersedes the older fact and records the provenance chain

Contradiction handling is where naive systems fail, and it is what the benchmark
weights most heavily.

## Forgetting

Memories carry a decay score driven by access recency, access frequency, and
age. Below a threshold they are evicted from the retrieval index. Forgetting is
not a nice-to-have — an agent that remembers everything retrieves badly.

## Measuring it

`bench/` generates synthetic multi-session conversations with planted facts,
planted contradictions, and planted updates, then scores:

| Metric | Question |
|---|---|
| Recall accuracy | Is the planted fact retrieved when it is needed? |
| Contradiction resolution | Does the system return the current fact, not the stale one? |
| Precision | How much retrieved context was irrelevant? |
| Token cost | Versus stuffing the full history into context |

The headline result is the recall/cost curve against that full-context baseline.
A memory system that is less accurate *and* cheaper is not interesting; the claim
has to be that it is competitive on accuracy at a fraction of the cost.

## Inspecting it

Aggregate scores say whether the system works. They do not say *why* a particular
fact won, and that is usually the question worth asking.

```bash
recall ui path/to/store.db
```

A read-only web UI over a store file:

- **Facts** — supersession chains rendered as chains. The Kingston fact and the
  Toronto fact that superseded it, side by side, each linked to the episode it
  came from.
- **Episodes** — the session timeline, and which facts each episode produced.
- **Retrieval** — run a query, see the ranked results with each score broken into
  its vector, recency, and frequency parts.
- **Decay** — decay scores over time against the eviction threshold, with evicted
  memories still visible and marked.
- **Benchmark** — the recall/cost curve against the full-context baseline.

Nothing in the UI writes to the store.

## Stack

- **Storage** — SQLite with `sqlite-vec`. One file, no daemon, real SQL for the
  metadata filtering and decay scoring that consolidation needs.
- **Embeddings** — `sentence-transformers`, local. No API key, so the benchmark
  runs on a clone.
- **Extraction and consolidation** — `claude-opus-5` with adaptive thinking.
- **Inspector** — FastAPI and React. The built frontend ships in the package, so
  running the UI needs no Node; building it does.

## Install

```bash
uv sync
uv run pytest
```

Extraction and consolidation need `ANTHROPIC_API_KEY`. Storage, retrieval, and
the embedding path run without it.

## Development

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if uv isn't installed
uv sync --all-extras
make check
```

`make check` runs the full gate — `ruff`, `ruff format --check`, `mypy --strict`,
`pytest` — which is exactly what CI runs. All four must pass before a commit.

The project pins `python-preference = "only-managed"`, so uv uses its own
interpreter rather than whatever is on `PATH`. This is not a style preference:
pyenv builds CPython without `--enable-loadable-sqlite-extensions` on macOS, and
an interpreter built that way cannot load `sqlite-vec` at all. Since the store is
built on that extension, the interpreter is not a free choice.

`uv.lock` is committed and CI installs with `--locked`. If you change a
dependency, run `uv sync --all-extras` and commit the updated lockfile in the
same change, or CI will fail on the stale lock.

## Status

Under active development. See `PLAN.md` for the milestone breakdown and
`PROGRESS.md` for the running log.

## License

MIT
