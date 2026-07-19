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
| 2026-07-18 | [eval/2026-07-18-expanded-set.md](eval/2026-07-18-expanded-set.md) | Eval set expanded 4 → 15 hard questions: hit@4 is structurally saturated at chapter level (3-file corpus), so purity (55/60) and first-hit rank (worst: 2) become the feature-gating metrics; Ch5/Ch6 vocabulary traps worked, semantic paraphrase did not |
| 2026-07-19 | [eval/2026-07-19-chunking-comparison.md](eval/2026-07-19-chunking-comparison.md) | Chunking sweep verdict: chunk size redistributes the cross-chapter confusion between rank and purity but never removes it — no config wins, 512/80 stays; the fix needs retrieval-side discrimination (hybrid/reranking) |
| 2026-07-19 | [eval/2026-07-19-chunking-512.md](eval/2026-07-19-chunking-512.md) | Sweep baseline leg (512/80): purity 55/60, mean rank 1.07 — identical to 2026-07-18, confirming retrieval determinism |
| 2026-07-19 | [eval/2026-07-19-chunking-256.md](eval/2026-07-19-chunking-256.md) | Sweep small leg (256/40, 386 chunks): purity unchanged, ranks worse (Q3 → rank 3) |
| 2026-07-19 | [eval/2026-07-19-chunking-1024.md](eval/2026-07-19-chunking-1024.md) | Sweep large leg (1024/160, 85 chunks): all ranks 1 and Q13 cleaned, but Q3/Q8 purity diluted to 1/4 |
| 2026-07-19 | [eval/2026-07-19-hybrid-comparison.md](eval/2026-07-19-hybrid-comparison.md) | Hybrid verdict: equal-weight RRF regresses purity 92% → 87% because the lexical side is strictly weaker (BM25-only 72%) and fails the Q8 trap identically to dense — dense stays, evidence now points to reranking |
| 2026-07-19 | [eval/2026-07-19-hybrid-dense-control.md](eval/2026-07-19-hybrid-dense-control.md) | Hybrid iteration control leg: reproduces the 512/80 baseline exactly (55/60, mean 1.07) |
| 2026-07-19 | [eval/2026-07-19-hybrid-rrf.md](eval/2026-07-19-hybrid-rrf.md) | Hybrid leg (dense + BM25, RRF k=60): 52/60 — one Q3 gain, four collateral losses, Q8 unmoved |
