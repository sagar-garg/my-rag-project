# Decision 005: Showcase-first direction and repo consolidation

## Status
Accepted (2026-07-18)

## Context

The project sat idle for roughly three months after Milestone 2. The latest real work — migrating from the deleted Qdrant Cloud cluster to a local embedded store, and moving assistant config from Cursor to Claude Code — existed only as uncommitted changes in one worktree. Branches had multiplied (`main`, `develop`, `feat/public-corpus-eval`, `codex/rag-v2`, `codex/rag-v2-wt`) while all pointing at the same commit.

Separately, a long-term goal was made explicit: this project should become a portfolio case study on my personal website, which means artifacts (eval results, screenshots, diagrams, narrative) must be collected continuously rather than reconstructed at the end.

## Decision

1. **Consolidate the repo**: commit the pending local-Qdrant and Cursor-to-Claude work, fast-forward `main`, delete the stale branches, and retire the extra worktree. `main` is the single source of truth going forward.
2. **Adopt a showcase-first build direction**: retrieval-quality features (hybrid search, reranking, richer retrieval-inspection UI) are now in scope. The gate is measurement, not minimalism — each feature ships with a before/after against the eval set.
3. **Institutionalize artifact collection**: `docs/showcase/` holds eval tables, screenshots, diagrams, and a living `case-study.md` draft. Every milestone deposits artifacts there (see CLAUDE.md "Showcase artifact habit").

## Why

- A case study built on measured iteration ("hit rate went from X to Y when I added Z") is far stronger portfolio evidence than a feature list — so the baseline eval run stays first on the roadmap even under showcase-first priorities.
- Uncommitted work in a side worktree is exactly the state the checkpoint/handoff system exists to prevent; consolidation restores the system's integrity.
- Collecting artifacts at milestone time is cheap; reconstructing them months later is expensive or impossible (e.g., screenshots of intermediate states).

## Alternatives considered

- Stay learning-first and defer showcase features:
  Safer scope, but the portfolio goal is the stated long-term purpose; deferring it just delays artifact collection that must start now anyway.
- Keep multiple branches/worktrees for parallel experiments:
  Unnecessary coordination overhead for a solo project with serial milestones.

## Consequences

- CLAUDE.md gains a showcase section; hybrid retrieval and reranking leave the "avoid" list and become eval-gated roadmap items.
- The roadmap is: baseline eval runner → expand eval set → chunking/hybrid/reranking iterations with measured deltas → UI polish → case-study assembly.
- Session handoffs should note which showcase artifacts were produced.
