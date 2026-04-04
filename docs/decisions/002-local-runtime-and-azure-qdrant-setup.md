# Decision 002: Local runtime and Azure/Qdrant setup for v1

## Status
Accepted

## Context

The first end-to-end smoke test exposed several integration issues that were not obvious from the code alone:

- the Streamlit entrypoint name conflicted with the top-level `app` package
- assistant-managed long-running processes introduced network/sandbox confusion during API debugging
- Azure embeddings and Azure Responses API had different setup requirements
- Qdrant Cloud configuration mixed up cluster URL, API key, and collection name

We want the project docs to preserve the simplest known-good local workflow.

## Decision

For local development in v1:

- run the app from the repo `.venv` in the user's own terminal
- use `app/ui/streamlit_app.py` as the Streamlit entrypoint
- treat Azure chat and embedding deployments as separate configuration values
- use `AZURE_OPENAI_API_VERSION=2025-03-01-preview` or later for Responses API support
- use Qdrant Cloud with a full HTTPS endpoint in `QDRANT_URL`
- keep `QDRANT_COLLECTION_NAME` as an application collection name, not a cluster name

## Why

- Running the app locally makes runtime behavior easier to reason about than assistant-managed background processes.
- A distinct Streamlit entrypoint avoids Python import shadowing against the `app` package.
- Azure embedding calls can work while Responses API calls fail, so generation must document its own API-version requirement.
- Qdrant setup is simpler when the app owns collection creation and the user only supplies endpoint, API key, and collection name.

## Alternatives considered

- Keep `app/ui/app.py` as the entrypoint:
  Rejected because it collided with the `app` package import path under Streamlit.
- Depend on assistant-launched background servers for normal local testing:
  Rejected because sandbox/network behavior made debugging less clear for a learning-first project.
- Reuse the chat deployment for embeddings:
  Rejected because embeddings and generation are different model roles.

## Consequences

- The documented local run command should prefer the repo `.venv`.
- Future setup docs should distinguish indexing failures from generation failures.
- The next datasets can focus on retrieval quality instead of basic infrastructure debugging.
