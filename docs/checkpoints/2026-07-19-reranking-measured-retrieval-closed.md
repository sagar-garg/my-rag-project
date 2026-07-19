# Reranking measured — split decision, retrieval-side iteration closed

## Date
2026-07-19

## Outcome
The third and final eval-gated retrieval iteration (ADR 005 roadmap item 3) shipped. An LLM listwise reranker — one `gpt-4o` chat call ranking dense's top-12 candidates down to top-4, zero new dependencies — was added as an opt-in path (`run_starter_eval --mode rerank`, `app/retrieval/rerank.py`) with dense untouched. Because the reranker is nondeterministic it was measured twice. Split decision: Q8, the Ch5/Ch6 acid test no previous change moved, went rank 2 → 1 in both runs, and Q3 went 2/4 → 4/4; but Q5 stably regressed (4/4 rank 1 → 3/4 rank 2), leaving aggregate purity at 55–56/60 vs dense's 55/60. Dense stays the default. With geometry (chunking), lexical signal (hybrid), and cross-attention reading (rerank) all measured, the residual ~8% impurity is reclassified as genuine cross-chapter content overlap — retrieval-side iteration on this corpus is closed.

## What works
- `app/retrieval/rerank.py` — `build_rerank_prompt` (numbered passages, no filenames, anti-injection instruction), `parse_ranking` (always returns a full permutation; falls back to dense order on garbage), `rerank_chunks` / `search_chunks_reranked` (token usage surfaced in `RerankResult`).
- `scripts/run_starter_eval.py --mode {dense,hybrid,rerank}` — rerank mode shares one Azure client, prints actual token usage per run.
- `extract_output_text` promoted to public in `app/generation/respond.py`, shared by generation and reranking.
- 34 tests green (9 new in `tests/test_rerank.py`, pure logic only, stub Azure client).
- Dense control reproduced the baseline exactly (55/60, mean 1.07, worst 2) before the reranker was judged; candidate-pool inspection verified Q8's purity was not candidate-capped (four Ch5 chunks in its top-12) and explained Q5's regression (two plausible off-target Ch5 chunks entered the widened pool).

## Corpus / data / inputs used
Chapters 4–6 PDFs, collection `book_chapters_4_6` (512/80, 176 chunks), 15-question eval set. Artifacts: `docs/showcase/eval/2026-07-19-rerank-{dense-control,llm,llm-run2,comparison}.md`. Cost: ~$0.43 (165,880 input + 1,114 output tokens on full-size `gpt-4o` across two runs) — the ledger's first non-trivial spend; actuals in `docs/costs.md`.

## Important lessons
- A reranker can only reorder what the candidate generator hands it — and the wider pool that lets it fix one question gives it rope to hang itself on another. Candidate depth is a hyperparameter with a failure mode, not free headroom.
- Nondeterministic components need repeat runs before judging: two runs separated stable effects (Q3 gain, Q8 rank fix, Q5 regression) from ±1-chunk jitter that a single run would have reported as signal.
- Check which deployment an env var points at before estimating cost: `AZURE_OPENAI_CHAT_DEPLOYMENT` was full-size `gpt-4o`, ~15× the assumed mini-tier price.
- When three different mechanisms leave the same residual error, stop blaming the component and re-examine the labels: the surviving impurity is chapters genuinely discussing overlapping material. Recognizing a metric's content ceiling is a finding, not a failure.
- Three iterations, one win-less arc, and the case study is stronger for it: measured nulls and split decisions demonstrate the discipline better than a lucky +1% would.

## Next step
UI polish (roadmap item 4): Streamlit retrieval inspector (scores, expected-vs-actual for eval questions, optional dense/hybrid/rerank toggle) and the first screenshots/GIFs into the still-empty `docs/showcase/assets/`. Presentation only — no retrieval-logic changes.
