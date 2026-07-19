# LLM listwise reranking (gpt-4o over dense top-12): split decision — dense stays the default — 2026-07-19

Third measured feature iteration (ADR 005 roadmap item 3), and the last of the
retrieval-side triangle: chunking ruled out geometry, hybrid ruled out lexical
signal, so this iteration tests the remaining hypothesis — a model that
*reads* each candidate against the question can separate the confusable
chapters. Setup: same collection (`book_chapters_4_6`, 512/80, 176 chunks),
same 15-question set; dense retrieves 12 candidates (top-4 × 3), a single
listwise chat call (`gpt-4o`, Responses API, no new dependencies) ranks them,
top-4 kept. Reranking is opt-in (`--mode rerank`); the dense path is untouched.

Because the reranker is nondeterministic, it was run **twice**. Per-run
artifacts: [dense control](2026-07-19-rerank-dense-control.md) ·
[rerank run 1](2026-07-19-rerank-llm.md) ·
[rerank run 2](2026-07-19-rerank-llm-run2.md).

## Aggregate results

| Metric | Dense (control) | Rerank run 1 | Rerank run 2 |
|--------|-----------------|--------------|--------------|
| Hit@4 | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Purity (on-target chunks) | **55/60 (92%)** | 56/60 (93%) | 55/60 (92%) |
| Mean first-hit rank | 1.07 | 1.07 | 1.07 |
| Worst first-hit rank | 2 (Q8) | 2 (Q5) | 2 (Q5) |

## The questions that moved

| Q | Target | Dense | Rerank run 1 | Rerank run 2 | Stable? |
|---|--------|-------|--------------|--------------|---------|
| Q3 — "two dominant patterns for context construction" | Ch6 | rank 1, 2/4 | rank 1, **4/4** | rank 1, **4/4** | ✅ stable gain |
| Q8 — "where in a long input…" (Ch5/Ch6 trap, the acid test) | Ch5 | **rank 2**, 2/4 | **rank 1**, 2/4 | **rank 1**, 3/4 | ✅ rank fix stable; purity jitters |
| Q5 — "how can you tell whether a model made something up" | Ch4 | rank 1, 4/4 | rank 2, **3/4** | rank 2, **3/4** | ❌ stable regression |
| Q9 — Santa / tone paraphrase | Ch5 | rank 1, 4/4 | rank 1, 4/4 | rank 1, 3/4 | ± jitter |
| Q13 — query rewriting (Ch4 leak) | Ch6 | rank 1, 3/4 | rank 1, 3/4 | rank 1, 2/4 | ± jitter |

## Observations

- **The acid test finally moved.** Q8's first-hit rank went 2 → 1 in *both*
  runs — the first retrieval-side change of three iterations to touch it.
  The hypothesis was right in kind: cross-attention reading does what neither
  embedding similarity nor term frequency could.
- **But the reranker giveth and the reranker taketh away.** Q5 regressed
  stably (4/4 rank 1 → 3/4 rank 2). Mechanism, verified by inspecting the
  candidate pool: dense's top-4 for Q5 was pure Ch4, but widening to 12
  candidates pulled in two Ch5 chunks, and the reranker promoted one to
  rank 1 — Ch5's prompt-engineering discussion of hallucination reads
  plausibly against a "did the model make something up" question. The wider
  candidate pool is a double-edged sword: it is what *allows* a reranker to
  fix Q8, and what *exposes* off-target text on questions dense had clean.
- **Q8's remaining impurity is not candidate-capped.** The dense top-12 for
  Q8 contains four Ch5 chunks, so 4/4 purity was available; the reranker
  picked 2–3 of them. Even reading the text, gpt-4o partially conflates
  Ch5's prompt-position advice with Ch6's long-context discussion — the same
  ambiguity that defeats embeddings and BM25 defeats a reader model less,
  but not fully.
- **Run-to-run jitter is ±1 chunk on ~3 questions** (Q8, Q9, Q13 differed
  between runs; Q3's gain and Q5's regression held). Aggregate purity
  55–56/60 vs dense's 55/60: within the noise band of a single run. Any
  future eval of a nondeterministic component needs repeat runs — one run
  at n=15 can't distinguish a +1 win from sampling luck.
- **Verdict: split decision; dense stays the default.** The stable wins
  (Q3 purity, Q8 rank) and the stable loss (Q5) roughly cancel in aggregate,
  and reranking costs ~$0.21 and ~15 s of chat latency per 15-question run
  (~$0.014 + 1–2 s per interactive query) for a net effect indistinguishable
  from zero on this eval set. The reranker stays in the code as `--mode
  rerank` — the honest summary for the case study is that at 92% purity on a
  three-chapter corpus, the residual errors look like genuine cross-chapter
  content overlap, which no retrieval-stage mechanism — geometry, lexical,
  or reader — cleanly removes.

## What this closes

Three iterations, three mechanisms, one conclusion: chunk geometry (null),
lexical signal (negative), cross-attention reranking (split). The Ch5/Ch6
confusion is now bounded as *content* ambiguity, not a retriever defect —
the remaining ~8% impurity is chunks from chapters that genuinely discuss
overlapping material. Retrieval-side iteration on this corpus has hit its
measurable ceiling; the next quality lever is generation-side (does the
answer use the retrieved context faithfully — Ragas) or presentation-side
(UI, case-study assembly).

## Cost

Two rerank runs: 165,880 input + 1,114 output tokens on `gpt-4o`
(~$0.21/run, **~$0.43 total** — the first non-trivial spend in the ledger);
dense control and candidate-pool inspection ≈ $0.0001. See `docs/costs.md`.
