---
name: next-milestone
description: Pick up this repository's work where the last session stopped and advance the next milestone. Use when the user says "continue", "next milestone", "keep going", or asks what state the project is in.
---

# Next milestone

Sessions on this repository start with no memory of the previous one.
`PROGRESS.md` is the handoff.

## Procedure

1. **Read `PROGRESS.md` bottom-up.** The last entry is where work stopped. Read
   at least the last two — the second-to-last often explains a decision the last
   one depends on.
2. **Read `PLAN.md`** for the milestone about to be worked. The plan is fixed; if
   its scope turns out to be wrong, say so and propose an amendment rather than
   silently doing something else.
3. **Confirm the working tree is clean** (`git status`). Uncommitted changes mean
   a previous session ended mid-work — read the diff before doing anything.
4. **Do the work.** Tests are written alongside the code, not deferred. A
   milestone is not done because the code exists; it is done when its
   "Done when" criterion in `PLAN.md` is demonstrably met.
5. **Run the full check** before committing:
   ```bash
   make check
   ```
   This runs `ruff`, `ruff format --check`, `mypy --strict`, and `pytest` — the
   same four CI runs. All four must pass. If something fails and cannot be fixed
   within scope, stop and record the failure in `PROGRESS.md` rather than
   committing over it.
6. **Commit.** Small, focused commits with imperative subjects
   (`add contradiction classifier`, not `Added contradiction classifier`).
   **Never add a `Co-Authored-By` trailer or any AI-attribution footer.**
7. **Append to `PROGRESS.md`**: what was built, what was decided and why, what is
   blocked, and what the next session should start on.
8. **Close the milestone's issue** with a comment summarizing the outcome.

## Rules specific to this repository

- **Once the benchmark exists, every change that claims an improvement reports a
  number.** Run it before and after; record both in `PROGRESS.md`. A change that
  "should help" and was not measured is not done.
- **Never tune against the held-out split.** Development uses the training
  conversations; the held-out set is touched only for the numbers that get
  published in `docs/results.md`.
- **Episodes are append-only.** No code path may edit or delete an episode's
  content. Corrections are new episodes; belief changes are fact supersessions.
- **Supersession preserves provenance.** `supersedes` and `superseded_by` are
  both written, and superseded facts stay in the store. Retrieval filters them
  out; storage does not discard them.
- **API calls use `claude-opus-5` with adaptive thinking.** Cache the stable
  instruction prefix. Consolidation is the expensive path — measure its token
  cost as deliberately as its accuracy.
- Storage, embedding, and retrieval must work without `ANTHROPIC_API_KEY`. Only
  extraction and consolidation may require it, and their absence must produce a
  clear error rather than a crash.
- **The inspector is read-only.** No endpoint it exposes may write to the store.
  It renders provenance; it is not a second path to mutating state alongside
  append-only episodes and supersession.
- **Running the UI must not require Node.** The built frontend ships in the
  package. If a change to the UI is not accompanied by a rebuilt bundle, CI
  fails — that is intended, not a nuisance to work around.
