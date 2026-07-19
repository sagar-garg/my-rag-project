# Hybrid retrieval measured and rejected — dense stays the default

## Date
2026-07-19

## Outcome
The second eval-gated feature iteration (ADR 005 roadmap item 3) shipped and produced a decisive negative result. A hand-rolled in-memory Okapi BM25 index plus reciprocal rank fusion was added as an opt-in retrieval path (`run_starter_eval --mode hybrid`, `search_chunks_hybrid`) with the dense path untouched. Against the 15-question eval set, equal-weight hybrid regressed purity from 55/60 (92%) to 52/60 (87%); a free BM25-only diagnostic measured the lexical side at 43/60 (72%) and showed it fails the worst question (Q8, the Ch5/Ch6 vocabulary trap) with the same wrong ranking as dense. Hybrid is rejected on evidence; the code remains as a documented control.

## What works
- `app/retrieval/lexical.py` — Okapi BM25 (tokenize, `Bm25Index`, paginated `load_corpus` scroll) built over the existing collection, no re-indexing, no API calls.
- `app/retrieval/fusion.py` — `reciprocal_rank_fusion`, pure function, deterministic tie-break.
- `app/retrieval/search.py` — `search_chunks_hybrid` (12 candidates/side, RRF k=60, top-4 out); dense `search_chunks` unchanged.
- `scripts/run_starter_eval.py --mode {dense,hybrid}` — both paths run against the same collection; artifact Configuration line reflects the mode.
- 25 tests green, including 14 new pure-function tests for BM25 and RRF (`tests/test_retrieval_fusion.py`).
- Dense control reproduced the chunking-sweep baseline exactly (55/60, mean rank 1.07, worst 2) before the hybrid leg was judged.

## Corpus / data / inputs used
Chapters 4–6 PDFs, collection `book_chapters_4_6` (512/80, 176 chunks), 15-question eval set `data/eval/chapters_4_6_starter.json`. Artifacts: `docs/showcase/eval/2026-07-19-hybrid-{dense-control,rrf,comparison}.md`. Cost ≈ $0.00002 (30 query embeddings).

## Important lessons
- When both retrievers agree on the wrong answer, no fusion can save you: the confusable chapters share their *distinctive* terms too, so BM25 reproduces dense's Q8 failure. Rank fusion only helps where retrievers disagree and the added one is right often enough.
- Measure a new component alone before fusing it: the free BM25-only diagnostic (72% purity) explained the hybrid regression immediately and proved no fusion weighting could win.
- An eval set built to defeat one retriever's weakness (paraphrase vs dense) stress-tests every later component for free.
- Negative results compound: chunking ruled out geometry, hybrid ruled out lexical signal — the fix space has narrowed to rerankers with more confidence than a single win would give.

## Next step
Reranking iteration: rerank dense top-12 down to top-4 with a model that reads candidate text against the question. Session-opening decision: local cross-encoder (heavy dependency, free per query) vs LLM reranker on the existing Azure chat deployment (no new dependency, chat cost per query). Q8 is the acid test.
