# Backlog

## Near-term priorities

- Run the chapter-based starter evaluation set against real retrieval outputs.
- Improve chunking once we have measured the Chapters 4-6 baseline.
- Add a small script or command for running evaluation outside the UI.

## Medium-term ideas

- Add a simple debug toggle in Streamlit to show retrieved chunks more explicitly.
- Add metadata filters if the next corpus has clear document categories.
- Add better chunking heuristics for longer documents.
- Expand the starter evaluation set once the first misses are understood.

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
