# Project State

_Last updated: 2026-07-19 (chunking sweep done — null result, 512/80 stays; next: hybrid retrieval)_

## Current status

- Minimal learning-first RAG app works end to end.
- **Chunking sweep done (2026-07-19) — first measured feature iteration, deliberate null result.** 256/40, 512/80, 1024/160 against the 15-question set: chunk size redistributes the Ch5/Ch6 confusion between rank and purity but never removes it (256: purity 55/60, worst rank 3; 512: 55/60, worst 2; 1024: 54/60, all ranks 1). **512/80 stays the default**; the Q3/Q8 fix needs retrieval-side discrimination — hybrid or reranking, the next roadmap item. Full analysis: `docs/showcase/eval/2026-07-19-chunking-comparison.md`.
- `run_starter_eval` now prints and writes an aggregate summary (purity, mean/worst first-hit rank) via `summarize_judgments()` in `app/eval/basic_eval.py` — per-run artifacts are one-glance comparable. Tested in `tests/test_basic_eval.py`.
- The local Qdrant store now holds three collections: `book_chapters_4_6` (512/80, the default), plus sweep leftovers `book_chapters_4_6_c256o40` and `book_chapters_4_6_c1024o160` (~$0.004 to rebuild if ever deleted; harmless to keep).
- **Eval set expanded to 15 questions** (`data/eval/chapters_4_6_starter.json`): 4 originals kept verbatim + 11 hard ones (no chapter names, paraphrased concepts, Ch5/Ch6 vocabulary traps, 2 cross-chapter targets). Artifact: `docs/showcase/eval/2026-07-18-expanded-set.md`.
- **Key finding: hit@4 is structurally unmissable at chapter granularity on a 3-file corpus** (all 4 chunks would have to land in the 2 wrong chapters). It stayed 15/15. The metrics features must move are **purity** (55/60 = 92%) and **first-hit rank** (worst: 2, on the Q8 Ch5/Ch6 trap; low-purity questions: Q3 2/4, Q8 2/4, Q13 3/4).
- `scripts/run_starter_eval.py` now takes `--title` for the artifact H1 (default "Retrieval eval").
- Earlier baseline (4 questions, saturated): `docs/showcase/eval/2026-07-18-baseline.md`.
- `search_chunks` accepts an optional shared Qdrant `client` (needed because the embedded store allows only one client instance even within a single process).
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

1. ~~**Baseline eval runner**~~ — done 2026-07-18: 4/4 hit@4 (saturated — see artifact).
2. ~~**Expand eval set**~~ — done 2026-07-18: 15 questions; hit@4 still 100% (structurally so), gating metrics now purity 55/60 and first-hit rank (worst 2).
3. **Measured iterations — now the priority** — ~~chunking~~ (done 2026-07-19, null result), hybrid retrieval (next), reranking; each with before/after vs the eval set, judged on purity and first-hit rank (hit@4 will read 100% → 100% regardless).
4. **UI polish** — retrieval inspector, demo-ready Streamlit; capture screenshots/GIF.
5. **Case-study assembly** — architecture diagram, narrative, export for website.

## Most important learnings so far

- Small clean corpora are best for first RAG smoke tests; debug retrieval and generation as separate stages.
- Changing corpora without a fresh collection name pollutes results with stale vectors.
- A tiny gold set is enough to start checking whether retrieval hits the intended chapter.
- Uncommitted work in side worktrees defeats the checkpoint system — commit at session end (learned the hard way, Apr→Jul gap).
- A 100% baseline is a finding, not a success: an eval set that can't produce misses can't measure improvement. Questions that quote chapter titles or reuse chapter vocabulary are trivially easy for dense retrieval.
- A metric that can't fail measures nothing: with 3 source files and top-4 retrieval, chapter-level hit@4 is near-unmissable. When the binary metric saturates structurally, move to the finer ones already being collected (purity, first-hit rank) before redesigning the eval.
- Embedding retrieval shrugs at paraphrase (the zero-overlap Santa question hit 4/4 rank 1) but stumbles on vocabulary shared across documents (Q8 "long input": rank 2, purity 2/4). Hard eval questions come from cross-document lexical overlap, not oblique wording.
- The embedded Qdrant lock is per client instance, not per process — building two clients in one script fails. Share one client (`search_chunks(..., client=...)`).
- Chunk size moves cross-chapter confusion around; it doesn't remove it. A geometry knob can't fix a discrimination problem — separating confusable chapters needs lexical signal (hybrid) or a reranker.
- Purity fractions aren't comparable across chunk sizes: 2/4 of 512-token chunks and 1/4 of 1024-token chunks are the same on-target tokens in twice the context. Compare configs on the same chunk size, or think in on-target tokens.
- Inline env vars beat `.env` for one-off config runs — `load_dotenv` doesn't override already-set variables, so `CHUNK_SIZE=… QDRANT_COLLECTION_NAME=… python -m …` sweeps configs without touching the file.
