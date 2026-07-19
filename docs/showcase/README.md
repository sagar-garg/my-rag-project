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
| 2026-07-19 | [eval/2026-07-19-rerank-comparison.md](eval/2026-07-19-rerank-comparison.md) | Rerank verdict: split decision — LLM listwise rerank (gpt-4o, dense top-12 → top-4) is the first change to move the Q8 acid test (rank 2 → 1, stable across two runs) and fixes Q3, but stably regresses Q5 and nets ~zero aggregate; dense stays the default, residual impurity reclassified as content ambiguity |
| 2026-07-19 | [eval/2026-07-19-rerank-dense-control.md](eval/2026-07-19-rerank-dense-control.md) | Rerank iteration control leg: reproduces the 512/80 baseline exactly (55/60, mean 1.07, worst 2) |
| 2026-07-19 | [eval/2026-07-19-rerank-llm.md](eval/2026-07-19-rerank-llm.md) | Rerank run 1: 56/60, Q3 4/4, Q8 rank 1, Q5 regressed to 3/4 rank 2 |
| 2026-07-19 | [eval/2026-07-19-rerank-llm-run2.md](eval/2026-07-19-rerank-llm-run2.md) | Rerank run 2 (stability check): 55/60 — Q3 gain and Q5 regression stable, ±1 chunk jitter on Q8/Q9/Q13 |
| 2026-07-19 | [eval/2026-07-19-rerank-gpt5mini-coda.md](eval/2026-07-19-rerank-gpt5mini-coda.md) | Rerank coda verdict: with `gpt-5-mini` as judge, first-hit rank saturates (1.00 both runs, no rank regressions) at ~¼ gpt-4o's cost, but purity is the same 55/60 wash — dense stays the default; gpt-5-mini strictly dominates gpt-4o as rerank judge, and the smoke test's perfect Q8 didn't replicate (n=1 lesson) |
| 2026-07-19 | [eval/2026-07-19-rerank-gpt5mini-run1.md](eval/2026-07-19-rerank-gpt5mini-run1.md) | gpt-5-mini rerank run 1: 55/60, all 15 first hits at rank 1 |
| 2026-07-19 | [eval/2026-07-19-rerank-gpt5mini-run2.md](eval/2026-07-19-rerank-gpt5mini-run2.md) | gpt-5-mini rerank run 2 (stability check): 55/60, all rank 1 again — rank saturation is stable, Q5/Q9 purity dips stable, Q3/Q8 jitter |
| 2026-07-19 | [assets/2026-07-19-inspector-clean-hit.png](assets/2026-07-19-inspector-clean-hit.png) | Retrieval inspector UI, clean hit (dense): green eval banner, purity 4/4, every chunk ✅ Ch4 |
| 2026-07-19 | [assets/2026-07-19-inspector-q8-dense.png](assets/2026-07-19-inspector-q8-dense.png) | The Q8 Ch5/Ch6 trap live in dense mode: rank-1 chunk flagged ❌ Ch6, banner shows hit at rank 2, purity 2/4 — the eval table's worst row, visible in the app |
| 2026-07-19 | [assets/2026-07-19-inspector-q8-rerank.png](assets/2026-07-19-inspector-q8-rerank.png) | Same question, rerank mode: ✅ Ch5 (the needle-in-a-haystack passage) promoted to rank 1, scores visibly out of dense order, token-cost readout on `gpt-5-mini` |
| 2026-07-19 | [assets/2026-07-19-mode-toggle.gif](assets/2026-07-19-mode-toggle.gif) | Demo GIF: Q8 asked in dense mode (rank-1 miss) → mode toggled to LLM rerank → rank-1 hit |
| 2026-07-19 | [architecture.mmd](architecture.mmd) · [assets/2026-07-19-architecture.svg](assets/2026-07-19-architecture.svg) | Stage-labeled architecture diagram (ingest → chunk → index → retrieve → generate, eval alongside): mermaid source + website-ready SVG export (neutral theme, transparent background) |
