# Backlog

## Near-term priorities

- Replace the smoke-test corpus with a narrow public job-related corpus.
- Add a tiny evaluation dataset with expected answers and target sources.
- Improve chunking once we have a more realistic corpus and can measure retrieval quality.

## Medium-term ideas

- Add a simple debug toggle in Streamlit to show retrieved chunks more explicitly.
- Add a small script or command for running evaluation outside the UI.
- Add metadata filters if the next corpus has clear document categories.
- Add better chunking heuristics for longer documents.

## Later ideas

- Compare retrieval quality across different chunk sizes and overlaps.
- Add reranking only if dense retrieval clearly becomes the bottleneck.
- Add a lightweight document quality checklist before indexing new corpora.

## Not for v1 unless clearly needed

- LiteLLM
- MCP
- DSPy
- GraphRAG
- multi-agent orchestration
- heavy observability or gateway layers
