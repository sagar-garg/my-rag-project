# Project State

## Current status

- Minimal learning-first RAG app works end to end.
- Azure OpenAI embeddings and Responses API are both working.
- Qdrant Cloud indexing and retrieval are working.
- Streamlit UI works when run locally from the repo `.venv`.

## Current architecture

- `app/ingest/`: local document loading and chunking
- `app/indexing/`: embedding plus Qdrant upsert
- `app/retrieval/`: top-k dense retrieval
- `app/generation/`: grounded prompt building plus Azure Responses API call
- `app/eval/`: minimal Ragas-ready dataset and evaluation wrapper
- `app/ui/`: Streamlit entrypoint and UI flow

## Current corpus

- Smoke-test corpus uses repo markdown docs copied into `data/raw/docs/`.
- This corpus is intentionally small and easy to inspect.

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

## Best next project direction

- Replace the smoke-test corpus with a narrow set of public job-related documents.
- Add a tiny hand-written evaluation set so retrieval quality can be judged intentionally.
