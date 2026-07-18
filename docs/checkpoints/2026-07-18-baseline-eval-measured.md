# Baseline retrieval eval measured — and saturated

## Date
2026-07-18

## Outcome
The first honest retrieval number exists: 4/4 (100%) hit@4 on the starter eval
set, with every first hit at rank 1. The runner (`scripts/run_starter_eval.py`)
is retrieval-only — 4 embedding calls, no chat API — and writes its results as
a markdown artifact. The number itself is the finding: the 4-question starter
set is too easy to measure anything, so expanding it is now the gate for all
feature work (ADR 005's eval-gated rule applied to the eval set itself).

## What works
- `.venv/bin/python -m scripts.run_starter_eval` — loads starter cases, runs
  dense top-4 retrieval per question, prints a hit/miss table, writes the
  artifact (default `docs/showcase/eval/<date>-baseline.md`, `--out` to
  override).
- `judge_retrieval()` in `app/eval/basic_eval.py` — pure hit@k judgment
  (hit, first-hit rank, on-target count), covered by 4 unit tests.
- `search_chunks(..., client=...)` — optional shared Qdrant client, so one
  process can check the collection and run many searches against the embedded
  store.
- First showcase artifact deposited: `docs/showcase/eval/2026-07-18-baseline.md`;
  artifact log and case-study timeline updated.

## Corpus / data / inputs used
Chapters 4–6 PDFs (collection `book_chapters_4_6`, chunk size 512 / overlap 80,
`text-embedding-3-small-2`), against the 4-question set in
`data/eval/chapters_4_6_starter.json`.

## Important lessons
- A 100% baseline is a finding, not a success — an eval set that can't produce
  misses can't measure improvement. Questions that name chapters or reuse
  chapter vocabulary are trivially easy for dense retrieval.
- The one crack: question 3 pulled 2/4 chunks from Chapter 5 for a Chapter 6
  question. Ch5/Ch6 vocabulary overlap is where harder questions live.
- The embedded Qdrant lock is per client *instance*, not per process — two
  clients in one script collide. Share one client across calls.

## Next step
Expand the eval set to ~12–15 harder questions (no chapter names, paraphrased
concepts, Ch5/Ch6 overlap traps), then re-measure — see
`prompts/current/next-chat.md`.
