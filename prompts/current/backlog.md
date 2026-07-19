# Backlog

## Near-term priorities

- **Azure model migration before 2026-10-01**: the `gpt-4o` chat deployment is deprecated (retires 2026-10-01, replacement gpt-5.1); gpt-4o-mini/gpt-4.1-mini retire the same month. Create a judge deployment on a GA mini (gpt-5-mini or gpt-5.4-mini) → `AZURE_OPENAI_JUDGE_DEPLOYMENT`, and migrate `AZURE_OPENAI_CHAT_DEPLOYMENT` to gpt-5.1 *before* any Ragas generation baselines are measured (a model swap mid-series breaks comparability). Source: Microsoft model-retirement schedule, checked 2026-07-19.

- ~~Build the baseline eval runner~~ — done 2026-07-18: 4/4 hit@4, saturated (`docs/showcase/eval/2026-07-18-baseline.md`).
- ~~Expand the eval set to ~12–15 harder questions~~ — done 2026-07-18: 15 questions (`docs/showcase/eval/2026-07-18-expanded-set.md`). Hit@4 is structurally saturated at chapter level; **purity (55/60) and first-hit rank (worst: 2) are now the gating metrics** for all feature work.
- ~~First measured iteration: chunking parameters~~ — done 2026-07-19: null result, 512/80 stays; chunk size redistributes the Ch5/Ch6 confusion, doesn't remove it (`docs/showcase/eval/2026-07-19-chunking-comparison.md`).
- ~~Add aggregate purity + mean first-hit rank to the runner's summary output~~ — done 2026-07-19 (`summarize_judgments`, Summary block in artifacts).
- ~~Hybrid retrieval (dense + lexical) with before/after numbers~~ — done 2026-07-19: negative result, rejected; BM25 side strictly weaker (72% purity) and fails Q8 identically to dense (`docs/showcase/eval/2026-07-19-hybrid-comparison.md`). Code stays opt-in (`--mode hybrid`) as documented control.
- ~~Reranking~~ — done 2026-07-19: split decision, stays opt-in (`--mode rerank`); Q8 rank fixed (stable) but Q5 stably regressed, aggregate a wash (`docs/showcase/eval/2026-07-19-rerank-comparison.md`). **Retrieval-side iteration closed** — residual impurity is content ambiguity, not a retriever defect.
- ~~Streamlit retrieval inspector~~ — done 2026-07-19: inspector + dense/hybrid/rerank toggle shipped; screenshots + demo GIF in `docs/showcase/assets/`; embedded-Qdrant lock race fixed via `st.cache_resource` shared client. Roadmap item 4 closed.
- ~~gpt-5-mini rerank coda~~ — done 2026-07-19: rank saturates (1.00 both runs, no regressions) at ~¼ cost, purity wash → dense stays default; gpt-5-mini strictly dominates gpt-4o as judge (`docs/showcase/eval/2026-07-19-rerank-gpt5mini-coda.md`).
- ~~Case-study assembly~~ — done 2026-07-19: architecture diagram (mermaid + SVG), narrative pass, learnings distilled; **export decision: markdown as-is** — `docs/showcase/` is canonical, website adaptation happens in the website repo. **ADR 005 roadmap complete.**
- **Azure model migration is now the next step** (gates Ragas) — see `prompts/current/next-chat.md`.

## Medium-term (showcase-first, eval-gated — ADR 005)
- Answer-quality metrics via Ragas (faithfulness, answer relevancy) — retrieval is now stable/closed. Judge calls can route to the cheap `gpt-5-mini` deployment (`AZURE_OPENAI_JUDGE_DEPLOYMENT`, live since 2026-07-19); **gate on migrating `AZURE_OPENAI_CHAT_DEPLOYMENT` to gpt-5.1 first** so the metric series isn't broken by the 2026-10-01 gpt-4o retirement.

## Showcase pipeline (continuous)

- Deposit an artifact in `docs/showcase/` at every milestone (see CLAUDE.md habit).
- ~~Architecture diagram exportable for the website~~ — done 2026-07-19 (`architecture.mmd` + `assets/2026-07-19-architecture.svg`).
- ~~Demo GIF of the UI once the retrieval inspector lands~~ — done 2026-07-19 (`assets/2026-07-19-mode-toggle.gif`).
- Case-study draft grows with each measured iteration.

## Later ideas

- Document quality checklist before indexing new corpora.
- Section-level or chunk-level gold labels — only if purity stops discriminating (rank and hit@4 already saturated); would let hit@k actually fail on this corpus.
- Rerank latency/cost knob: `reasoning={"effort": "low"}` on the gpt-5-mini judge call (~1k reasoning tokens/call is the cost driver) — untested, only worth it if rerank mode gets real interactive use.

## Still out of scope unless clearly needed

- LiteLLM, MCP, DSPy, GraphRAG, multi-agent orchestration, heavy observability layers.
