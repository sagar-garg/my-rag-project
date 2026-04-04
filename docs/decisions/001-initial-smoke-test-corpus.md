# Decision 001: Initial smoke-test corpus

## Status
Accepted

## Context

We need a first dataset for local RAG testing that is small, public, easy to inspect, and unlikely to fail because of messy extraction.

## Decision

Use the repository's own markdown documentation as the initial smoke-test corpus by copying the current `docs/` markdown files into `data/raw/docs/`.

## Why

- Markdown is cleaner than scanned or image-heavy PDFs.
- The content is already public and directly relevant to the app.
- Retrieval quality is easy to judge because we know the source material.
- Small, readable files make debugging chunking and citations much easier.

## Alternatives considered

- Public job-related documents:
  Good next step once the pipeline works, because the corpus will be more realistic and personally useful.
- Books or long PDF guides:
  Useful later, but they introduce extraction noise too early for a first smoke test.

## Consequences

- Early tests should focus on correctness, not breadth.
- After the smoke test passes, we should move to a narrow set of public job-related documents for more realistic evaluation.
