# Milestone 2: Chapters 4-6 Corpus Baseline

## Date

2026-04-09

## Outcome

The app now uses a narrow three-PDF corpus from Chapters 4, 5, and 6 as its default learning baseline, and the repo includes a tiny hand-written evaluation starter set.

## What changed

- default raw corpus path now points to `data/raw/docs/`
- default source selection now targets the three chapter PDFs explicitly
- default Qdrant collection name now separates this baseline from the original smoke test
- starter evaluation cases now live in `data/eval/chapters_4_6_starter.json`
- evaluation helpers can load starter cases and turn them into runtime `EvalSample` records

## Why this matters

- the corpus is still small enough to inspect manually
- the content is much better aligned with retrieval, prompting, and evaluation questions
- source expectations are clearer because each chapter has a distinct theme
- the starter eval set gives us a baseline before changing chunking or retrieval strategy

## Important lessons

- explicit corpus selection matters once a raw-data folder starts collecting unrelated files
- changing corpora without changing the Qdrant collection risks stale vectors polluting results
- a tiny gold set is enough to start evaluating retrieval intentionally

## Next step

Run the chapter-based eval starter against actual retrieval outputs, then improve chunking only if the baseline exposes clear misses.
