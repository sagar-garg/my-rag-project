# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `docs/showcase/eval/2026-07-19-hybrid-comparison.md` (why hybrid lost and what it proves)

Now start the next measured feature iteration — **reranking**, roadmap item 3 of ADR 005 continued.

Context: two negative results triangulate here. Chunking (2026-07-19) ruled out geometry; hybrid (2026-07-19) ruled out lexical signal — BM25 fails the Q8 Ch5/Ch6 trap with the *same wrong ranking* as dense, because the confusable chapters share their distinctive vocabulary. What's left is a model that actually reads candidate text against the question. Baseline to beat (512/80, dense top-4): purity 55/60 (92%), mean first-hit rank 1.07, worst 2; weak questions Q3 (2/4), Q8 (2/4, rank 2), Q13 (3/4).

Goals:

- rerank the dense top-N candidates (N ≈ 12, reuse `CANDIDATE_MULTIPLIER` from `app/retrieval/search.py`) down to top-4; keep dense top-4 as the control, reranking opt-in (`--mode` pattern already exists in `scripts/run_starter_eval.py`)
- **plan first — the reranker choice is the session's main decision.** Two candidates, each violating one project preference: a local cross-encoder (e.g. a small BGE/MiniLM reranker) is free per query but drags in a heavy dependency (torch/sentence-transformers) against the minimal-deps rule; an LLM reranker uses the existing Azure chat deployment (zero new deps) but adds a chat call per query and per eval question. Lay out the tradeoff with estimated eval-run cost before touching anything; the call is Sagar's.
- run dense control + reranked eval with `--out docs/showcase/eval/2026-MM-DD-rerank-<variant>.md`; judge on purity and first-hit rank for Q3/Q8/Q13 — Q8 is the acid test (the one failure no retriever-side change has moved)
- comparison artifact + showcase README log + case-study timeline; ADR via `/record` if reranking wins (it would settle roadmap item 3)
- unit tests for any pure logic (prompt formatting / score parsing / candidate truncation) — no API calls in tests, per `tests/test_generation.py` pattern

Requirements:

- stop Streamlit first (embedded Qdrant single-process lock); share one Qdrant client
- if the LLM route is chosen: estimate cost up front (15 questions × ~12 candidates), append actuals to `docs/costs.md`; retrieval-only eval must stay cheap
- state the verification checks up front (pytest + eval Summary tables as evidence; dense control must reproduce purity 55/60, mean 1.07, worst 2 before judging the reranker)
- end with /handoff
