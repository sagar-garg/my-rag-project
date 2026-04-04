# RAG stack for this project

## Goal
Build a simple educational RAG app in 1-2 weeks.

## Stack
- LlamaIndex for the RAG pipeline
- Qdrant as the vector store
- Azure OpenAI Responses API for generation
- Ragas for evaluation
- Streamlit for UI

## Why this stack
- Simple enough to finish quickly
- Teaches core RAG concepts
- Keeps architecture understandable
- Good tradeoff between speed and learning

## First milestone
- Load local docs
- Chunk them
- Embed them
- Store them in Qdrant
- Retrieve top-k chunks
- Generate answer using retrieved context
- Show sources in Streamlit

## Current status
- The first milestone now works end to end on a small smoke-test corpus.
- The initial corpus is the repo's own markdown docs copied into `data/raw/docs/`.
- Azure embeddings, Qdrant indexing, retrieval, grounded generation, and source display all work together.

## What we learned from milestone one
- Keep the first corpus small and inspectable so debugging stays about the pipeline, not messy documents.
- Retrieval can work even when generation is broken, so test those stages separately.
- Azure embedding setup and Azure Responses API setup have different failure modes.
- Running the app locally from `.venv` is simpler to reason about than relying on assistant-managed long-running processes.

## Later improvements
- metadata filters
- hybrid retrieval
- better chunking
- Ragas evaluation

## Next natural step
- Move from the smoke-test corpus to a narrow set of public job-related documents.
- Add a tiny hand-written evaluation set so retrieval and answer quality can be judged intentionally rather than by impression alone.