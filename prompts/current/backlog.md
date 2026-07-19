# Backlog

## Near-term priorities

- ~~Build the baseline eval runner~~ — done 2026-07-18: 4/4 hit@4, saturated (`docs/showcase/eval/2026-07-18-baseline.md`).
- ~~Expand the eval set to ~12–15 harder questions~~ — done 2026-07-18: 15 questions (`docs/showcase/eval/2026-07-18-expanded-set.md`). Hit@4 is structurally saturated at chapter level; **purity (55/60) and first-hit rank (worst: 2) are now the gating metrics** for all feature work.
- ~~First measured iteration: chunking parameters~~ — done 2026-07-19: null result, 512/80 stays; chunk size redistributes the Ch5/Ch6 confusion, doesn't remove it (`docs/showcase/eval/2026-07-19-chunking-comparison.md`).
- ~~Add aggregate purity + mean first-hit rank to the runner's summary output~~ — done 2026-07-19 (`summarize_judgments`, Summary block in artifacts).
- ~~Hybrid retrieval (dense + lexical) with before/after numbers~~ — done 2026-07-19: negative result, rejected; BM25 side strictly weaker (72% purity) and fails Q8 identically to dense (`docs/showcase/eval/2026-07-19-hybrid-comparison.md`). Code stays opt-in (`--mode hybrid`) as documented control.
- ~~Reranking~~ — done 2026-07-19: split decision, stays opt-in (`--mode rerank`); Q8 rank fixed (stable) but Q5 stably regressed, aggregate a wash (`docs/showcase/eval/2026-07-19-rerank-comparison.md`). **Retrieval-side iteration closed** — residual impurity is content ambiguity, not a retriever defect.
- **Streamlit retrieval inspector — now the next step** (roadmap item 4): scores, chunk boundaries, expected-vs-actual sources for eval questions; optional dense/hybrid/rerank mode toggle; capture screenshots/GIF for `docs/showcase/assets/`. See `prompts/current/next-chat.md`.

## Medium-term (showcase-first, eval-gated — ADR 005)
- Answer-quality metrics via Ragas (faithfulness, answer relevancy) — retrieval is now stable/closed. Cost caveat: the chat deployment is full-size `gpt-4o` (~$2.50/1M input); estimate per-metric cost first, consider a mini deployment for judge calls.

## Showcase pipeline (continuous)

- Deposit an artifact in `docs/showcase/` at every milestone (see CLAUDE.md habit).
- Architecture diagram exportable for the website.
- Demo GIF of the UI once the retrieval inspector lands.
- Case-study draft grows with each measured iteration.

## Later ideas

- Document quality checklist before indexing new corpora.
- Section-level or chunk-level gold labels — only if purity/rank stop discriminating; would let hit@k actually fail on this corpus.

## Still out of scope unless clearly needed

- LiteLLM, MCP, DSPy, GraphRAG, multi-agent orchestration, heavy observability layers.
