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
