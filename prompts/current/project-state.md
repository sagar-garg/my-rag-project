# Project State

_Last updated: 2026-07-20 (website integration shipped; next: Azure model migration, the Ragas gate)_

## Current status

- Minimal learning-first RAG app works end to end.
- **Website integration shipped (2026-07-20) — the last open showcase thread, now closed.** The case study is live as a native page in the portfolio repo (`showcase-my-vision`) at `/projects/rag-first-principles`, sourced from `docs/showcase/case-study.md`. The markdown-as-is export decision held: no export tooling was needed here, and nothing in this repo changed. **Asset lesson worth carrying forward:** four of the five showcase assets could not be used on the site. `2026-07-19-architecture.svg` is `fill:#000000` on a transparent background at 2229×477 — invisible on a dark page and unreadable at any phone width; the light-theme Streamlit PNGs were ~8px-illegible at the width they'd actually render. Both were rebuilt natively in JSX from the underlying numbers, so only `2026-07-19-mode-toggle.gif` was consumed. If a future asset is intended for the website, author it dark-theme-safe and closer to 1:1. The site also links `docs/walkthrough.md` as its primary "go deeper" CTA.
- **Case study assembled (2026-07-19) — ADR 005 roadmap item 5 done, roadmap complete.** `docs/showcase/case-study.md` is now a full draft: tightened pitch (three honest negatives bound the residual error as content ambiguity), new "The arc" narrative section with the Q8 dense/rerank screenshots embedded, finalized engineering-decisions section, and seven distilled "Learnings worth publishing". Architecture diagram: mermaid source `docs/showcase/architecture.mmd` (neutral theme, edge-order tuned so the pipeline stays on one rank) + SVG export `docs/showcase/assets/2026-07-19-architecture.svg`. All relative links verified; 42 tests green, zero code changes. **Export decision (Sagar, 2026-07-19): markdown as-is** — `docs/showcase/` is the canonical artifact; adaptation happens in the website repo, no export tooling here.
- **Rerank coda done (2026-07-19, later same day) — gpt-5-mini judge, two runs, verdict narrows but stands.** The smoke test's perfect Q8 did *not* replicate (2–3/4 purity), aggregate purity a 55/60 wash both runs — but **all 15 questions hit first-hit rank 1 in both runs** (dense worst: 2; gpt-4o rerank worst: 2), no rank regressions, at ~$0.05/run (~¼ of gpt-4o). Pre-registered flip criteria (Q5 recovered, aggregate > dense) not met → dense stays the default, no ADR; gpt-5-mini strictly dominates gpt-4o as rerank judge. Full analysis: `docs/showcase/eval/2026-07-19-rerank-gpt5mini-coda.md`. Untested knob: `reasoning={"effort": "low"}` in `rerank_chunks` (~1k reasoning tokens/call is the cost driver).
- **Retrieval inspector UI + mode toggle shipped (2026-07-19) — ADR 005 roadmap item 4 done.** Streamlit now has a sidebar retrieval-mode radio (dense default / hybrid / rerank with cost caption) and a per-query inspector: chunk rank, chapter label, chunk index, score (with per-mode score caption — `RetrievedChunk.score` is cosine for dense, RRF for hybrid, dense-passthrough for rerank), eval-question matching with expected-vs-actual ✅/❌ highlighting and a hit/rank/purity banner (`judge_retrieval` reused). Pure helpers in `app/ui/inspector.py` (`chapter_label` — moved from the eval script, `find_matching_case`, `score_caption`), tested in `tests/test_inspector.py`. **42 tests green.**
- **Embedded-Qdrant lock race found and fixed while driving the app:** Streamlit reruns can briefly overlap (cooperative cancellation), so per-rerun `QdrantClient` creation races for the store's flock → `RuntimeError: Storage folder … already accessed`. Fix: one process-wide client via `@st.cache_resource get_qdrant_client()`; the rebuild-index button closes + clears it first because `build_index` opens its own client. Also: `$` in `st.caption` strings triggers LaTeX math rendering — escape as `\\$`.
- **Showcase assets captured (2026-07-19) — `docs/showcase/assets/` no longer empty:** clean-hit and Q8-dense/Q8-rerank inspector screenshots + a 4-frame mode-toggle GIF (Q8 dense miss → rerank fix), captured by driving the live app with Playwright; logged in `docs/showcase/README.md`, referenced from `case-study.md` (new timeline rows + a "judge model is a hyperparameter" failure-lesson entry).
- **LLM reranking done (2026-07-19) — third and final retrieval-side iteration, split decision, dense stays the default.** Listwise gpt-4o rerank of dense top-12 → top-4 (`app/retrieval/rerank.py`, opt-in via `--mode rerank`, zero new deps; robust ranking parse falls back to dense order). Run twice (nondeterministic): Q8's rank finally moved (2 → 1, stable — the only change of three iterations to do it) and Q3 fixed (4/4), but Q5 stably regressed (wider candidate pool exposed plausible Ch5 text); aggregate purity 55–56/60 vs dense 55/60 — a wash. **Retrieval-side iteration closed: the residual ~8% impurity is cross-chapter content overlap, not a retriever defect.** Cost surprise: the chat deployment is full-size `gpt-4o`, so the two runs cost ~$0.43 (ledger's first real spend — see `docs/costs.md`). Full analysis: `docs/showcase/eval/2026-07-19-rerank-comparison.md`.
- **Hybrid retrieval done (2026-07-19) — second measured iteration, negative result, hybrid rejected.** Hand-rolled in-memory Okapi BM25 (`app/retrieval/lexical.py`) + reciprocal rank fusion (`app/retrieval/fusion.py`), opt-in via `search_chunks_hybrid` and `run_starter_eval --mode hybrid`; dense path untouched. Purity: dense 55/60 (92%) vs hybrid 52/60 (87%) vs BM25-only 43/60 (72%). BM25 fails the Q8 Ch5/Ch6 trap identically to dense, so no fusion weighting can rescue it. **Dense stays the default; the evidence now points to reranking.** Full analysis: `docs/showcase/eval/2026-07-19-hybrid-comparison.md`.
- **Chunking sweep done (2026-07-19) — first measured feature iteration, deliberate null result.** 256/40, 512/80, 1024/160 against the 15-question set: chunk size redistributes the Ch5/Ch6 confusion between rank and purity but never removes it (256: purity 55/60, worst rank 3; 512: 55/60, worst 2; 1024: 54/60, all ranks 1). **512/80 stays the default**; the Q3/Q8 fix needs retrieval-side discrimination — hybrid or reranking, the next roadmap item. Full analysis: `docs/showcase/eval/2026-07-19-chunking-comparison.md`.
- `run_starter_eval` now prints and writes an aggregate summary (purity, mean/worst first-hit rank) via `summarize_judgments()` in `app/eval/basic_eval.py` — per-run artifacts are one-glance comparable. Tested in `tests/test_basic_eval.py`.
- The local Qdrant store now holds three collections: `book_chapters_4_6` (512/80, the default), plus sweep leftovers `book_chapters_4_6_c256o40` and `book_chapters_4_6_c1024o160` (~$0.004 to rebuild if ever deleted; harmless to keep).
- **Eval set expanded to 15 questions** (`data/eval/chapters_4_6_starter.json`): 4 originals kept verbatim + 11 hard ones (no chapter names, paraphrased concepts, Ch5/Ch6 vocabulary traps, 2 cross-chapter targets). Artifact: `docs/showcase/eval/2026-07-18-expanded-set.md`.
- **Key finding: hit@4 is structurally unmissable at chapter granularity on a 3-file corpus** (all 4 chunks would have to land in the 2 wrong chapters). It stayed 15/15. The metrics features must move are **purity** (55/60 = 92%) and **first-hit rank** (worst: 2, on the Q8 Ch5/Ch6 trap; low-purity questions: Q3 2/4, Q8 2/4, Q13 3/4).
- `scripts/run_starter_eval.py` now takes `--title` for the artifact H1 (default "Retrieval eval").
- Earlier baseline (4 questions, saturated): `docs/showcase/eval/2026-07-18-baseline.md`.
- `search_chunks` accepts an optional shared Qdrant `client` (needed because the embedded store allows only one client instance even within a single process).
- Vector store is now a **local embedded Qdrant** (`QDRANT_LOCAL_PATH=qdrant_data`); the cloud cluster was deleted. Single-process caveat: stop Streamlit before running `build_index` or `scripts.inspect_store`.
- Azure OpenAI embeddings and Responses API working (separate deployments). **Judge-call routing (2026-07-19):** optional `AZURE_OPENAI_JUDGE_DEPLOYMENT` (currently `gpt-5-mini`, same resource) backs rerank/eval-judge calls via `config.judge_deployment_name`, falling back to the chat deployment when unset; user-facing answers stay on `AZURE_OPENAI_CHAT_DEPLOYMENT` (`gpt-4o` — **deprecated on Azure, retires 2026-10-01**, migrate to gpt-5.1 before Ragas baselines; see backlog).
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
3. ~~**Measured iterations**~~ — **complete 2026-07-19**: ~~chunking~~ (null), ~~hybrid~~ (rejected), ~~reranking~~ (split decision, opt-in). Three mechanisms — geometry, lexical, reader — bound the residual impurity as content ambiguity; retrieval-side work on this corpus is closed.
4. ~~**UI polish**~~ — done 2026-07-19: retrieval inspector + dense/hybrid/rerank toggle in Streamlit; screenshots + demo GIF in `docs/showcase/assets/`.
5. ~~**Case-study assembly**~~ — done 2026-07-19: diagram, narrative, learnings; export = markdown as-is (Sagar's call). **Roadmap complete.** Next frontier: Azure model migration → Ragas generation metrics (see backlog).

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
- When both retrievers agree on the wrong answer, no fusion can save you: BM25 fails the Q8 vocabulary trap with the same wrong ranking as dense, because the confusable chapters share their *distinctive* terms too. Rank fusion only helps where the retrievers disagree and the added one is right often enough.
- An eval set designed to defeat one retriever's weakness (paraphrase vs dense) also stress-tests every later feature — BM25's 72% purity on paraphrased questions was predictable in hindsight; check a new component alone (the free BM25-only diagnostic) before blaming the fusion.
- Negative results compound: chunking ruled out geometry, hybrid ruled out lexical signal — two cheap nulls narrowed the fix to rerankers more convincingly than one win would have.
- A reranker can only reorder what the candidate generator hands it — and the wider pool that lets it fix one question (Q8's four on-target chunks in the top-12) gives it rope to hang itself on another (Q5's two plausible off-target chunks). Candidate depth is a real hyperparameter, not just headroom.
- A nondeterministic component demands repeat runs before judging: one 15-question run can't tell a +1 purity win from sampling luck. Two runs separated the stable effects (Q3 gain, Q8 rank fix, Q5 regression) from ±1 jitter (Q8/Q9/Q13).
- Check which deployment an env var points at before estimating LLM cost — `AZURE_OPENAI_CHAT_DEPLOYMENT` turned out to be full-size `gpt-4o`, ~15× the assumed mini-tier price ($0.21 vs $0.015 per rerank run).
- When three different mechanisms leave the same residual error, stop blaming the component and re-examine the labels: the surviving ~8% impurity is chunks from chapters that genuinely discuss overlapping material. Knowing when a metric has hit its content ceiling is itself a finding.
- The judge model is a hyperparameter: swapping gpt-4o → gpt-5-mini in the *same* rerank prompt saturated first-hit rank (1.00 both runs, no regressions) at ¼ the cost. And an n=1 smoke test misleads — the perfect Q8 it showed didn't survive two full runs.
- A saturated metric stops discriminating and can be retired: first-hit rank joined hit@4 (under gpt-5-mini rerank); purity is the only metric with headroom left on this corpus.
- Streamlit reruns overlap briefly (cooperative cancellation), so any resource that allows one live instance per process — like the embedded Qdrant client — must be `st.cache_resource`-shared, not created per rerun; per-rerun creation races intermittently, failing on the *first* click but not the second.
