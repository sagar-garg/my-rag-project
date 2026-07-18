# Backlog

## Near-term priorities

- Build the baseline eval runner (`scripts/run_starter_eval.py`): retrieval-only pass over the starter questions, per-question chapter hit/miss table, saved to `docs/showcase/eval/`.
- Inspect misses by chapter; expand the starter eval set to ~12–15 questions.
- First measured iteration: chunking parameters vs the baseline.

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
