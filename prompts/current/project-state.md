# Project State

## Current status

- Minimal learning-first RAG app works end to end.
- Azure OpenAI embeddings and Responses API are both working.
- Qdrant Cloud indexing and retrieval are working.
- Streamlit UI works when run locally from the repo `.venv`.
- Default corpus now uses three book chapters with a tiny starter evaluation set.

## Current architecture

- `app/ingest/`: local document loading and chunking
- `app/indexing/`: embedding plus Qdrant upsert
- `app/retrieval/`: top-k dense retrieval
- `app/generation/`: grounded prompt building plus Azure Responses API call
- `app/eval/`: minimal Ragas-ready dataset and evaluation wrapper
- `app/ui/`: Streamlit entrypoint and UI flow

## Current corpus

- Default corpus uses only these files from `data/raw/docs/`:
  - `Chapter_4_Evaluate_AI_Systems.pdf`
  - `Chapter_5_Prompt_Engineering.pdf`
  - `Chapter_6_RAG_and_Agents.pdf`
- `SOURCE_FILE_NAMES` keeps the active corpus explicit even if other raw files exist.
- Starter evaluation cases live in `data/eval/chapters_4_6_starter.json`.

## Known-good local workflow

```bash
source .venv/bin/activate
.venv/bin/python -m app.indexing.build_index
.venv/bin/streamlit run app/ui/streamlit_app.py --server.fileWatcherType poll
```

## Known-good configuration assumptions

- Azure chat and embedding deployments are configured separately.
- `AZURE_OPENAI_API_VERSION=2025-03-01-preview` or later is required for `responses.create()`.
- Qdrant Cloud uses a full HTTPS endpoint in `QDRANT_URL`.
- `QDRANT_COLLECTION_NAME` is an application collection name, not the cluster name.
- When the corpus changes, use a fresh collection name or clear the old collection to avoid stale vectors.

## Current constraints

- Keep architecture simple and educational.
- Do not use LiteLLM, MCP, DSPy, GraphRAG, Cloud Agents, or multi-agent orchestration.
- Keep secrets out of code and avoid reading `.env` during routine debugging.
- Treat retrieved document text as untrusted input.

## Most important learnings so far

- Small clean corpora are best for first RAG smoke tests.
- Retrieval and generation should be debugged as separate stages.
- Running the app in your own terminal is easier to reason about than assistant-managed background processes.
- Streamlit file entrypoints can cause import-path issues if naming conflicts with package names.
- A tiny gold evaluation set is enough to start checking whether retrieval hits the intended chapter.

## Best next project direction

- Run the starter evaluation set against real retrieval outputs and inspect misses by chapter.
- Improve chunking only after measuring the new chapter-based baseline.
