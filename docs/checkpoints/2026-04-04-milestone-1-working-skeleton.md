# Milestone 1: Working Skeleton

## Date

2026-04-04

## Outcome

The first version of the learning-first RAG app works end to end on a small smoke-test corpus.

## What works

- document loading from `data/raw/`
- chunking and indexing
- Azure embeddings
- Qdrant Cloud storage and retrieval
- grounded answer generation through Azure OpenAI Responses API
- Streamlit UI with answer and source display

## Corpus used

- repo markdown docs copied into `data/raw/docs/`

## Important lessons

- start with a small clean corpus
- separate chat and embedding deployments in Azure
- use `2025-03-01-preview` or later for Azure Responses API
- keep Qdrant endpoint, API key, and collection name conceptually separate
- prefer local `.venv` app runs during cloud debugging

## Next step

Move to a narrow real-world public corpus and add a tiny evaluation starter set.
