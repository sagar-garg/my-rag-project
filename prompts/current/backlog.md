# Backlog

## Near-term priorities

- ~~Build the baseline eval runner~~ — done 2026-07-18: 4/4 hit@4, saturated (`docs/showcase/eval/2026-07-18-baseline.md`).
- ~~Expand the eval set to ~12–15 harder questions~~ — done 2026-07-18: 15 questions (`docs/showcase/eval/2026-07-18-expanded-set.md`). Hit@4 is structurally saturated at chapter level; **purity (55/60) and first-hit rank (worst: 2) are now the gating metrics** for all feature work.
- **First measured iteration: chunking parameters** vs the 15-question set, judged on purity/first-hit rank. Weak questions to watch: Q3, Q8, Q13.
- Add aggregate purity + mean first-hit rank to the runner's summary output (makes per-run comparison one-glance).

## Medium-term (showcase-first, eval-gated — ADR 005)

- Hybrid retrieval (dense + sparse) with before/after numbers.
- Reranking, if eval misses show dense/hybrid retrieval is the bottleneck.
- Streamlit retrieval inspector: show scores, chunk boundaries, expected-vs-actual sources for eval questions.
- Answer-quality metrics via Ragas (faithfulness, answer relevancy) once retrieval is stable.

## Showcase pipeline (continuous)

- Deposit an artifact in `docs/showcase/` at every milestone (see CLAUDE.md habit).
- Architecture diagram exportable for the website.
- Demo GIF of the UI once the retrieval inspector lands.
- Case-study draft grows with each measured iteration.

## Later ideas

- Compare chunk sizes/overlaps systematically.
- Document quality checklist before indexing new corpora.
- Section-level or chunk-level gold labels — only if purity/rank stop discriminating; would let hit@k actually fail on this corpus.

## Still out of scope unless clearly needed

- LiteLLM, MCP, DSPy, GraphRAG, multi-agent orchestration, heavy observability layers.
