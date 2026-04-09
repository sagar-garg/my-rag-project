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
- The app now uses a narrow three-document PDF corpus from Chapters 4, 5, and 6 of the book in `data/raw/docs/`.
- Azure embeddings, Qdrant indexing, retrieval, grounded generation, and source display all work together on this corpus.
- A tiny hand-written evaluation starter set now lives in `data/eval/chapters_4_6_starter.json`.

## What we learned from milestone one
- Keep the first corpus small and inspectable so debugging stays about the pipeline, not messy documents.
- Retrieval can work even when generation is broken, so test those stages separately.
- Azure embedding setup and Azure Responses API setup have different failure modes.
- Running the app locally from `.venv` is simpler to reason about than relying on assistant-managed long-running processes.
- Explicit corpus selection matters once `data/raw/` starts to accumulate more files.

## Later improvements
- metadata filters
- hybrid retrieval
- better chunking
- richer Ragas evaluation

## Next natural step
- Run the starter evaluation set against real retrieval outputs and inspect which questions miss their target chapter.
- Improve chunking only after the chapter-based baseline has been measured.