# Working with Cursor in this repo

This is a learning-first RAG project.

## What I want
- I want to build fast, but I also want to understand what is happening.
- I prefer simple, educational code over clever abstractions.
- I want short explanations whenever an important technical choice is made.
- I want recommendations for better Cursor usage when relevant, but not repetitive nagging.

## How to help me
- Before major work, give a short plan.
- When introducing a concept, explain it briefly.
- When there are alternatives, recommend the simplest path unless a more advanced path is clearly justified.
- Keep dependencies minimal.
- Update docs when code changes significantly.

## End-of-chat workflow
- Before ending a substantial chat, update durable learnings in `docs/`.
- Update `prompts/current/project-state.md` with the current repo state.
- Update `prompts/current/next-chat.md` with the best next prompt.
- Update `prompts/current/backlog.md` if priorities changed.
- Add a checkpoint in `docs/checkpoints/` when a milestone is reached.

## Current stack
- Azure OpenAI Responses API
- LlamaIndex
- Qdrant
- Ragas
- Streamlit

## What to avoid unless explicitly requested
- LiteLLM
- MCP
- Cloud Agents
- DSPy
- GraphRAG
- multi-agent orchestration
- unnecessary JS frameworks