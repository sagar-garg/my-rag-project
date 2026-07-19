# Chunking sweep measured — null result, 512/80 stays

## Date
2026-07-19

## Outcome

The first measured feature iteration under ADR 005 is complete: three chunking
configurations (256/40, 512/80, 1024/160 — overlap held at ~15.6% of size)
were each indexed into a fresh local-Qdrant collection and evaluated against
the 15-question set on purity and first-hit rank. No configuration beats the
512/80 baseline overall, and the default stays unchanged. The negative result
is itself the finding: chunk geometry redistributes the cross-chapter
vocabulary confusion between the two metrics but never removes it, so the
Q3/Q8 fix must come from retrieval-side discrimination (hybrid or reranking).

## What works

- Config sweeps without touching `.env`: inline env vars
  (`CHUNK_SIZE=… CHUNK_OVERLAP=… QDRANT_COLLECTION_NAME=…`) override the file
  because `load_dotenv` never overwrites already-set variables.
- `scripts.run_starter_eval` prints and writes an aggregate Summary block
  (purity, mean/worst first-hit rank) via `summarize_judgments()` in
  `app/eval/basic_eval.py` — per-run artifacts are directly comparable.
  Covered by unit tests (11 passing).
- Retrieval is deterministic run-to-run: the re-run 512/80 leg reproduced the
  2026-07-18 numbers exactly (purity 55/60, mean rank 1.07, worst 2).
- Full sweep cost ≈ $0.004 (two re-indexes ≈ 190k embedded tokens + 45 query
  embeds), logged in `docs/costs.md`.

## Corpus / data / inputs used

Chapters 4–6 PDFs; 15-question eval set
(`data/eval/chapters_4_6_starter.json`); collections `book_chapters_4_6`
(176 chunks), `book_chapters_4_6_c256o40` (386), `book_chapters_4_6_c1024o160`
(85). Results: `docs/showcase/eval/2026-07-19-chunking-comparison.md`.

## Important lessons

- **Chunk size moves the failure around; it doesn't remove it.** Off-target
  Ch5/Ch6 chunks stayed in the top-4 for the trap questions at every size:
  256/40 traded Q8's rank for Q3's (rank 3, the sweep's worst cell); 1024/160
  put every first hit at rank 1 but diluted Q3/Q8 purity to 1/4. A geometry
  knob can't fix a discrimination problem.
- **Purity fractions don't compare across chunk sizes.** 2/4 of 512-token
  chunks and 1/4 of 1024-token chunks are the *same* on-target tokens in twice
  the context. Compare configs at fixed chunk size, or reason in on-target
  tokens — and remember bigger chunks ≈ proportionally bigger generation
  prompts and chat cost.
- **A null result recorded is progress.** The sweep cost half a cent, ruled
  out a whole parameter axis, and sharpened the hypothesis for the next
  feature (lexical signal discriminates confusable chapters; embeddings
  alone don't).

## Next step

Hybrid retrieval (dense + lexical fusion) against the same baseline, judged on
whether it cleans up Q3/Q8/Q13 purity and holds rank 1 — prompt ready in
`prompts/current/next-chat.md`.
