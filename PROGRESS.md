# Progress log

Append-only. Newest entry at the bottom.

The purpose of this file is continuity: a session that starts cold reads the last
entry and knows where the work stopped, what was decided, and what is blocked.
Record decisions and their reasons, not just what was written — the file list is
already in the git log.

---

## Scaffold

Repository created. Structure, tooling, and CI in place; no memory code yet.

**Decided:**
- SQLite + `sqlite-vec` over Postgres/pgvector or LanceDB. Consolidation needs
  relational queries as much as vector search, and a single-file store means
  anyone can clone and run the benchmark with no daemon.
- Local `sentence-transformers` embeddings rather than a hosted embedding API,
  so the benchmark reproduces without a second API key. Costs a torch
  dependency; worth it for a repo meant to be run by strangers.
- The benchmark lands at milestone 3, before consolidation and forgetting. Every
  claim here is comparative, so the measuring instrument comes first.
- Episodic memory is append-only. Corrections supersede rather than edit, which
  keeps the provenance chain intact for contradiction handling.

**Next:** Milestone 1, the storage layer. See `PLAN.md`.

---

## Plan revision — the inspector

No code. `PLAN.md` grew from seven milestones to eight: a read-only web UI is now
milestone 7, and results and interface moved to 8.

**Decided:**
- The system's distinctive behaviour is invisible in aggregate numbers. A recall
  score of 0.84 does not show that the Kingston fact was superseded by the
  Toronto fact and that retrieval correctly returned the second — a supersession
  chain on a screen does. The inspector exists to make the mechanism legible, not
  to make the repository look finished.
- It goes after forgetting, not before. Built any earlier it would have nothing
  to render: no provenance chains until milestone 5, no decay curves until 6.
- It goes before the results writeup rather than after, because `docs/results.md`
  and the README both want figures and this is what produces them.
- React and Vite over server-rendered templates. Costs a build step in a Python
  repository, which is a real cost — the tension is with the milestone-8 promise
  that a stranger can clone and reproduce the headline number.
- That tension is resolved by shipping the built frontend inside the Python
  package: `uv sync && recall ui` works with no npm install, and CI rebuilds and
  fails if the committed build is stale. Node is a prerequisite for contributing
  to the UI, not for running it.
- The API is read-only by construction, not by convention. Episodes are
  append-only and supersession is the only way a belief changes; an inspector
  with write endpoints would be a second path to mutating state that bypasses
  both invariants.

**Next:** Milestone 1, the storage layer. Unchanged — the revision affects the
back half of the plan only.

---

## Chore — local toolchain

No milestone code. The full gate now runs locally; before this it ran only in CI.

**Decided:**
- `python-preference = "only-managed"`. This started as a chore and turned into a
  real finding: pyenv builds CPython without
  `--enable-loadable-sqlite-extensions` on macOS, so `sqlite3.Connection` has no
  `enable_load_extension` attribute at all and `sqlite-vec` cannot be loaded. The
  entire store depends on that extension, so the interpreter is not a free
  choice. uv's managed builds have it; pinning removes the dependency on however
  a contributor happened to build their Python.
- This would not have been caught in CI. CI runs `uv python install 3.12`, which
  gets a managed build and works. The bug was local-only, which is precisely the
  divergence that makes "CI is the real check" a bad position to stay in.
- `uv.lock` committed and CI switched to `uv sync --all-extras --locked`.
  `--locked` fails the build when the lock has drifted from `pyproject.toml`;
  `--frozen` would have used a stale lock silently. Milestone 8 promises a
  stranger can clone and reproduce the headline number, and an unpinned
  `sentence-transformers` would move the embeddings underneath the benchmark.
- `make check` is now the single definition of the gate, referenced by the
  `next-milestone` skill instead of a copy-pasted command chain, so local and CI
  cannot drift.

**Verified:** `sqlite-vec` v0.1.9 loads on arm64 macOS under the managed
interpreter, and a `vec0` virtual table accepts an insert and returns the
expected row from a KNN query. Milestone 1 is unblocked.

**Next:** Milestone 1, the storage layer. See `PLAN.md`.
