# Project State

_Last updated: 2026-07-18 (repo consolidation + showcase-first direction, ADR 005)_

## Current status

- Minimal learning-first RAG app works end to end.
- Vector store is now a **local embedded Qdrant** (`QDRANT_LOCAL_PATH=qdrant_data`); the cloud cluster was deleted. Single-process caveat: stop Streamlit before running `build_index` or `scripts.inspect_store`.
- Azure OpenAI embeddings and Responses API working (separate deployments).
- Default corpus: Chapters 4–6 PDFs with a 4-question starter eval set in `data/eval/chapters_4_6_starter.json`.
- Repo consolidated onto `main`; stale branches deleted; the `-wt` worktree retired.
- Assistant config migrated from Cursor to Claude Code (`CLAUDE.md`) / Codex (`AGENTS.md`); Cursor rules archived in `docs/archive/cursor/`.

## Long-term goal (new)

Portfolio case study for the personal website. `docs/showcase/` collects artifacts continuously (eval tables → `eval/`, screenshots/GIFs → `assets/`, living draft in `case-study.md`). Direction is showcase-first but eval-gated: every retrieval feature ships with a measured before/after. See ADR 005.

## Current architecture

- `app/ingest/` → `app/indexing/` → Qdrant → `app/retrieval/` → `app/generation/` → `app/ui/` (Streamlit), with `app/eval/` (Ragas-ready) alongside. `scripts/inspect_store.py` peeks at stored points.

## Known-good local workflow

```bash
source .venv/bin/activate
.venv/bin/python -m app.indexing.build_index
.venv/bin/streamlit run app/ui/streamlit_app.py --server.fileWatcherType poll
.venv/bin/python -m scripts.inspect_store   # free, local-only
```

## Roadmap (ADR 005)

1. **Baseline eval runner** — script that runs the 4 starter questions through retrieval, reports per-question chapter hit/miss, saves the table to `docs/showcase/eval/`. First honest number.
2. **Expand eval set** to ~12–15 questions once misses are understood.
3. **Measured iterations** — chunking, hybrid retrieval, reranking; each with before/after vs the eval set.
4. **UI polish** — retrieval inspector, demo-ready Streamlit; capture screenshots/GIF.
5. **Case-study assembly** — architecture diagram, narrative, export for website.

## Most important learnings so far

- Small clean corpora are best for first RAG smoke tests; debug retrieval and generation as separate stages.
- Changing corpora without a fresh collection name pollutes results with stale vectors.
- A tiny gold set is enough to start checking whether retrieval hits the intended chapter.
- Uncommitted work in side worktrees defeats the checkpoint system — commit at session end (learned the hard way, Apr→Jul gap).
