# Milestone 3: Repo consolidation and showcase-first direction

## Date

2026-07-18

## Outcome

After a three-month pause, the repo is consolidated onto `main` with all pending work committed, and the project has an explicit long-term goal: a portfolio case study for the personal website (ADR 005).

## What changed

- Committed the previously uncommitted local-Qdrant migration (`QDRANT_LOCAL_PATH`, embedded store; cloud cluster was deleted).
- Committed the Cursor → Claude Code / Codex config migration (`CLAUDE.md`, `AGENTS.md`, archived `.cursor/rules/`).
- Fast-forwarded `main`, deleted stale branches (`develop`, `feat/public-corpus-eval`, `codex/*`), retired the extra worktree.
- Created `docs/showcase/` (artifact log, `eval/`, `assets/`, living `case-study.md`) and the artifact-collection habit in CLAUDE.md.
- Updated `prompts/current/` state files for the new direction.

## Important lessons

- Uncommitted work in a side worktree silently breaks the handoff system; the Apr→Jul gap was only reconstructible from the git diff.
- A portfolio showcase is strongest as a byproduct of measured iteration — collect artifacts at milestone time, don't reconstruct later.

## Next step

Build the baseline eval runner: retrieval-only pass over the 4 starter questions, hit/miss by chapter, saved as the first showcase artifact.
