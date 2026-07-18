# Case study: building and measuring a RAG system from first principles

> Living draft. Sections fill in as milestones land; artifacts referenced from `eval/` and `assets/`.

## The pitch (draft)

A RAG system built stage by stage — loading, chunking, indexing, retrieval, grounded generation — where every quality improvement was driven by a hand-built evaluation set, not vibes. Corpus: three chapters of Chip Huyen's *AI Engineering* (evaluation, prompt engineering, RAG & agents) — small enough to inspect by hand, real enough to expose retrieval failures.

## Architecture

_TODO: exportable diagram (mermaid → SVG for the website). Base on the flowchart in README.md._

Stack: Python, LlamaIndex Core, Qdrant (local embedded), Azure OpenAI (separate embedding + chat deployments, Responses API), Ragas, Streamlit.

## Timeline of measured iterations

| Milestone | Date | Retrieval hit rate | Notes |
|-----------|------|--------------------|-------|
| Working skeleton | 2026-04-04 | — | end-to-end pipeline on smoke corpus |
| Real corpus + gold set | 2026-04-09 | — | chapters 4–6, 4 starter questions |
| Baseline measured | _pending_ | _pending_ | first honest number |

## Interesting failures and fixes

_TODO: populate from eval misses — this section is where the story lives._

## Key engineering decisions

Source: `docs/decisions/` (ADRs 001–005). Candidates for the write-up:

- explicit corpus selection + fresh collection names to avoid stale-vector pollution
- separating retrieval debugging from generation debugging
- local embedded vector store over cloud for a single-user learning system
- eval-gated feature additions (ADR 005)

## Learnings worth publishing

_TODO: distill from `docs/checkpoints/` "Important lessons" sections at assembly time._
