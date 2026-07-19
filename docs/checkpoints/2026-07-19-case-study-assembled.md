# Case study assembled — ADR 005 roadmap complete

## Date
2026-07-19

## Outcome
The portfolio case study is a complete draft: `docs/showcase/case-study.md` now has a finished pitch, an exportable architecture diagram, a five-act narrative of the measured-iteration arc with the Q8 dense-vs-rerank screenshots embedded, finalized engineering decisions, and seven distilled publishable learnings. This closes roadmap item 5 of ADR 005 — all five items are done. Export target (Sagar's decision): markdown as-is; `docs/showcase/` is the canonical artifact and any adaptation happens in the website repo.

## What works
- Architecture diagram: mermaid source (`docs/showcase/architecture.mmd`, neutral theme) exports cleanly via mermaid-cli to `docs/showcase/assets/2026-07-19-architecture.svg`; rendered output visually verified.
- `case-study.md` is self-contained for a markdown-native site: every relative link (5 assets + 6 eval artifacts + diagram source) verified to resolve.
- Test suite untouched and green (42 tests) — the session was writing/diagram only, zero code changes.

## Corpus / data / inputs used
Assembled from the 18 dated artifacts in `docs/showcase/` (14 eval files, 4 UI assets), the checkpoint log, and `prompts/current/project-state.md` learnings. No new eval runs.

## Important lessons
- Assembly was cheap because collection was continuous: the artifact-habit rule (no milestone without a deposited artifact) meant the case study was curation, not reconstruction.
- A win-less arc writes a better case study than a lucky win: three measured negatives that bound the residual error tell a stronger story than "+1% purity" would have.
- Mermaid/dagre layout is steerable without hacks: declare the main pipeline as one edge chain first and keep side-branch nodes out of subgraphs — subgraph height, not edge order alone, is what pushes stages off the main rank.

## Next step
Azure model migration (`gpt-4o` chat deployment retires 2026-10-01 → `gpt-5.1`), which gates the first Ragas generation baseline — see `prompts/current/next-chat.md`.
