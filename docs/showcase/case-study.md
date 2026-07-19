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
| Chunking sweep (256/512/1024) | 2026-07-19 | purity 92% / 92% / 90%, mean rank 1.13 / 1.07 / 1.00 | first measured feature iteration — and a deliberate null result: chunk size redistributes the Ch5/Ch6 confusion between rank and purity but never removes it; 512/80 kept, fix deferred to hybrid/reranking ([details](eval/2026-07-19-chunking-comparison.md)) |
| Hybrid retrieval (dense + BM25, RRF) | 2026-07-19 | purity 92% (dense) vs 87% (hybrid) vs 72% (BM25-only) | second negative result, hybrid rejected on evidence: the lexical side is strictly weaker on a paraphrase-heavy eval set and fails the Ch5/Ch6 trap identically to dense, so equal-weight fusion pollutes four clean questions to gain one chunk; dense stays, and two nulls now triangulate the fix to reranking ([details](eval/2026-07-19-hybrid-comparison.md)) |
| LLM listwise reranking (gpt-4o, dense top-12 → top-4) | 2026-07-19 | purity 92% (dense) vs 93% / 92% (rerank ×2 runs) | split decision: the first change to move the Q8 acid test (rank 2 → 1, stable across both runs) and a full Q3 fix, but a stable Q5 regression cancels the gains — the wider candidate pool that lets a reranker fix one question exposes off-target text on another; dense stays the default, and the residual ~8% impurity is reclassified as genuine cross-chapter content overlap, closing retrieval-side iteration ([details](eval/2026-07-19-rerank-comparison.md)) |

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
- **Chunk size moves the failure around; it doesn't remove it.** Sweeping
  256/512/1024-token chunks against the same eval set, the two Ch5/Ch6-trap
  questions kept off-target chunks in the top-4 in *every* config — smaller
  chunks traded one question's rank for another's, larger chunks fixed every
  rank while diluting purity (and would double per-answer context cost). A
  geometry knob can't fix a discrimination problem: separating confusable
  chapters needs lexical signal (hybrid) or a reranker. Also a measurement
  lesson: purity fractions aren't comparable across chunk sizes — 2/4 of
  512-token chunks and 1/4 of 1024-token chunks are the *same* on-target
  tokens in twice the context. (2026-07-19)
- **When both retrievers agree on the wrong answer, no fusion can save you.**
  Hybrid dense+BM25 via reciprocal rank fusion was supposed to separate the
  confusable chapters through distinctive-term weighting. Measured: BM25-only
  purity 72% vs dense 92% on a deliberately paraphrase-heavy eval set, and on
  the worst question (Q8) BM25 produced the *same* wrong ranking as dense —
  the chapters share their distinctive vocabulary too. Equal-weight RRF
  therefore averaged a strong ranking with a weak one: one chunk gained, four
  lost. The negative result is more useful than a win would have been: chunk
  geometry and lexical signal are both ruled out, which narrows the fix to a
  reranker that reads candidate text against the question. (2026-07-19)
- **The reranker giveth and the reranker taketh away.** An LLM listwise
  reranker (gpt-4o reading dense's top-12, one chat call per question, zero
  new dependencies) was the first change in three iterations to move the
  hardest question: Q8's first-hit rank went 2 → 1 in both runs. But it
  stably broke a question dense had perfect: widening the candidate pool
  from 4 to 12 exposed two plausible-reading off-target chunks on Q5, and
  the reranker promoted one to rank 1. Net aggregate effect ≈ zero
  (55–56/60 vs 55/60), at ~$0.014 + 1–2 s per query. Two structural
  lessons: a reranker can only reorder what the candidate generator hands
  it, and the wider pool that gives it room to fix one question gives it
  rope to hang itself on another. A nondeterministic component also forced
  a measurement upgrade — repeat runs, separating stable effects from ±1
  jitter. Three mechanisms later (geometry, lexical, reader), the residual
  ~8% impurity looks like genuine cross-chapter content overlap, not a
  retriever defect: retrieval-side iteration on this corpus closed here.
  (2026-07-19)

## Key engineering decisions

Source: `docs/decisions/` (ADRs 001–005). Candidates for the write-up:

- explicit corpus selection + fresh collection names to avoid stale-vector pollution
- separating retrieval debugging from generation debugging
- local embedded vector store over cloud for a single-user learning system
- eval-gated feature additions (ADR 005)

## Learnings worth publishing

_TODO: distill from `docs/checkpoints/` "Important lessons" sections at assembly time._
