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
| Baseline measured | 2026-07-18 | 4/4 (100%) hit@4 | starter set saturated — all first hits at rank 1; eval set must get harder before features can show gains ([details](eval/2026-07-18-baseline.md)) |
| Eval set expanded 4 → 15 | 2026-07-18 | 15/15 (100%) hit@4, purity 55/60 (92%) | hit@4 turns out to be structurally unmissable at chapter level on a 3-file corpus; purity and first-hit rank (worst: 2, on the designed Ch5/Ch6 trap) are now the metrics features must move ([details](eval/2026-07-18-expanded-set.md)) |

## Interesting failures and fixes

_Populating from eval near-misses; this section is where the story lives._

- **A metric that can't fail measures nothing.** Hit@4 at chapter granularity on
  a 3-file corpus is structurally unmissable — all four retrieved chunks would
  have to come from the two wrong chapters. Expanding the eval set from 4 to 15
  much harder questions left it at 100%; the real signal moved to chunk purity
  (55/60) and first-hit rank. (2026-07-18)
- **Dense retrieval shrugs at paraphrase but stumbles on shared vocabulary.**
  The question written with *zero* lexical overlap with its target passage
  ("the bot ruins the magic for children" → the Santa/fictional-characters
  example) retrieved perfectly. The question that reused vocabulary two chapters
  share ("where in a long input should information go?" — prompt-position advice
  in Ch5 vs long-context-vs-RAG in Ch6) produced the first rank-2 result and
  2/4 purity. Hardness for embeddings is cross-document lexical confusion, not
  obliqueness. (2026-07-18)

## Key engineering decisions

Source: `docs/decisions/` (ADRs 001–005). Candidates for the write-up:

- explicit corpus selection + fresh collection names to avoid stale-vector pollution
- separating retrieval debugging from generation debugging
- local embedded vector store over cloud for a single-user learning system
- eval-gated feature additions (ADR 005)

## Learnings worth publishing

_TODO: distill from `docs/checkpoints/` "Important lessons" sections at assembly time._
