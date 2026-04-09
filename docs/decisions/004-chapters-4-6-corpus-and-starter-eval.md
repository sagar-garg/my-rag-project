# Decision 004: Chapters 4-6 corpus and starter evaluation set

## Status
Accepted

## Context

The initial smoke-test corpus proved that the RAG pipeline worked, but it was too close to the repo itself to teach much about realistic retrieval quality. We needed a next-step corpus that stayed small and inspectable while being rich enough to support targeted evaluation questions.

## Decision

Use these three PDFs in `data/raw/docs/` as the default corpus:

- `Chapter_4_Evaluate_AI_Systems.pdf`
- `Chapter_5_Prompt_Engineering.pdf`
- `Chapter_6_RAG_and_Agents.pdf`

Also add a tiny hand-written evaluation starter set in `data/eval/chapters_4_6_starter.json` with:

- a question
- a reference answer
- expected source file names

## Why

- The three chapters are thematically coherent around evaluation, prompting, and RAG.
- They are narrow enough to inspect manually, but more realistic than indexing only repo docs.
- The chapter boundaries make source expectations easy to reason about during retrieval checks.
- A tiny on-disk evaluation file is easier to extend and review than hardcoded ad-hoc samples.

## Alternatives considered

- Keep using repo markdown docs:
  Too easy and too tied to the implementation itself for the next learning step.
- Index the whole book:
  More realistic, but larger than needed for the first intentional evaluation pass.
- Build a full evaluation runner now:
  Useful later, but unnecessary before we have a stable tiny gold set.

## Consequences

- The default `.env.example` now points to `data/raw/docs/` and the three chapter file names.
- Swapping corpora should also mean using a fresh `QDRANT_COLLECTION_NAME` or clearing the old collection.
- Future evaluation work can focus on running retrieval against this gold set before changing chunking or adding reranking.
