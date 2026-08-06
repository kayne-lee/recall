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
