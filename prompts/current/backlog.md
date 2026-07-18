# Backlog

## Near-term priorities

- ~~Build the baseline eval runner~~ — done 2026-07-18: 4/4 hit@4, saturated (`docs/showcase/eval/2026-07-18-baseline.md`).
- **Expand the eval set to ~12–15 harder questions** (no chapter names, paraphrased concepts, Ch5/Ch6 overlap traps). This gates everything below — a saturated eval can't measure improvement.
- First measured iteration: chunking parameters vs the (new, harder) baseline.

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

## Still out of scope unless clearly needed

- LiteLLM, MCP, DSPy, GraphRAG, multi-agent orchestration, heavy observability layers.
