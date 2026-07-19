# Hybrid retrieval (dense + BM25 via RRF): dense wins — 2026-07-19

Second measured feature iteration (ADR 005 roadmap item 3), second negative
result. Hypothesis under test: BM25-style lexical scoring discriminates
between chapters that share vocabulary better than embeddings alone, because
the *distinctive* terms of the target passage get weighted up. Setup: same
collection (`book_chapters_4_6`, 512/80, 176 chunks), same 15-question set,
hand-rolled Okapi BM25 in memory (no re-indexing, no API cost), equal-weight
reciprocal rank fusion (k=60), 12 candidates per side, top-4 returned.

Per-run artifacts: [dense control](2026-07-19-hybrid-dense-control.md) ·
[hybrid RRF](2026-07-19-hybrid-rrf.md). The BM25-only column is a free local
diagnostic (no embedding calls), run to explain the hybrid regression.

## Aggregate results

| Metric | Dense (control) | Hybrid (RRF) | BM25-only (diagnostic) |
|--------|-----------------|--------------|------------------------|
| Hit@4 | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Purity (on-target chunks) | **55/60 (92%)** | 52/60 (87%) | 43/60 (72%) |
| Mean first-hit rank | 1.07 | 1.07 | 1.40 |
| Worst first-hit rank | 2 | 2 | 3 |

## The three target questions — and the collateral damage

| Q | Target | Dense | Hybrid (RRF) | BM25-only |
|---|--------|-------|--------------|-----------|
| Q3 — "two dominant patterns for context construction" | Ch6 | rank 1, 2/4 | rank 1, **3/4** ✚ | rank 1, 3/4 |
| Q8 — "where in a long input…" (Ch5/Ch6 trap) | Ch5 | rank 2, 2/4 | rank 2, 2/4 (unchanged) | rank 2, 2/4 |
| Q13 — query rewriting (Ch4 leak) | Ch6 | rank 1, 3/4 | rank 1, **2/4** ▼ | rank 2, 1/4 |
| Q7 — "how many examples before I trust a comparison" | Ch4 | rank 1, 4/4 | rank 1, **3/4** ▼ | rank 2, 2/4 |
| Q9 — Santa / tone-without-retraining paraphrase | Ch5 | rank 1, 4/4 | rank 1, **3/4** ▼ | rank 1, 2/4 |
| Q10 — prompt-extraction attack | Ch5 | rank 1, 4/4 | rank 1, **3/4** ▼ | rank 1, 3/4 |

Net: hybrid gained one on-target chunk (Q3) and lost four (Q7, Q9, Q10, Q13).

## Observations

- **The lexical side is strictly weaker on this eval set: 72% purity vs
  dense's 92%.** Equal-weight RRF averages a strong ranking with a weak one,
  so the fusion inherited BM25's noise on four questions that dense had
  clean. The one gain (Q3) doesn't cover the losses.
- **The hypothesis is falsified where it matters most: Q8.** BM25 fails the
  Ch5/Ch6 trap *identically* to dense (rank 2, purity 2/4, same Ch6-first
  pattern). Shared vocabulary across chapters — "long input", "context",
  "position" — confuses term-frequency scoring just as it confuses
  embeddings. The distinctive-terms-get-weighted-up story doesn't play out,
  because the confusable passages share their distinctive terms too.
- **The eval set was built to defeat lexical matching, and it does.** 11 of
  15 questions are deliberate paraphrases with little vocabulary overlap
  with their target passages (the design lesson of 2026-07-18). BM25 only
  sees query terms; where the question avoids the passage's words, BM25
  votes on noise (Q13: purity 1/4, promoting Ch5/Ch4 chunks that merely
  reuse "questions"/"results" wording).
- **No fusion weighting rescues this.** Down-weighting the lexical side
  converges back to dense; up-weighting it makes the regression worse. And
  on the one question that matters most (Q8), both retrievers agree on the
  wrong ranking, so any rank fusion of the two reproduces the failure.
- **Verdict: dense stays the default; hybrid rejected on evidence.** Two
  null/negative results in a row (chunking, hybrid) now triangulate the fix:
  the Ch5/Ch6 confusion survives chunk geometry *and* lexical signal — what
  remains is a model that actually reads the candidate text against the
  question, i.e. a **reranker** (cross-encoder locally, or LLM-based),
  which is the next roadmap item. The hybrid path stays in the code
  (`--mode hybrid`, opt-in, dense untouched) as the documented control.

## Cost

Two eval runs (30 query embeddings ≈ 1k tokens) ≈ **$0.00002**; BM25 and RRF
are pure local computation — see `docs/costs.md`.
