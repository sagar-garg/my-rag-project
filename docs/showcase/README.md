# Showcase artifacts

Raw material for the portfolio case study (target: personal website). Collected continuously — see "Showcase artifact habit" in CLAUDE.md.

## Layout

- `case-study.md` — the living write-up draft; artifacts below feed it
- `eval/` — eval results per iteration: hit-rate tables, Ragas metrics, before/after comparisons. One file per run, named `YYYY-MM-DD-<what-changed>.md`
- `assets/` — screenshots, demo GIFs, exported diagrams. Same date-prefixed naming.

## Artifact log

| Date | Artifact | What it shows |
|------|----------|---------------|
| 2026-07-18 | [eval/2026-07-18-baseline.md](eval/2026-07-18-baseline.md) | Baseline retrieval eval: 4/4 hit@4, all first hits at rank 1 — the starter set is saturated; expanding it is the gate for feature work |
