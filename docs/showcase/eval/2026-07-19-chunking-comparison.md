# Chunking sweep: 256 vs 512 vs 1024 — 2026-07-19

First measured feature iteration (ADR 005 roadmap item 3). Three chunking
configurations, same 15-question eval set, same embedding model
(`text-embedding-3-small-2`), dense top-4. Overlap held at ~15.6% of chunk
size throughout, so each build embeds roughly the same total tokens — only
chunk count changes.

Per-run artifacts: [256/40](2026-07-19-chunking-256.md) ·
[512/80 baseline](2026-07-19-chunking-512.md) ·
[1024/160](2026-07-19-chunking-1024.md)

## Aggregate results

| Metric | 256/40 | 512/80 (baseline) | 1024/160 |
|--------|--------|-------------------|----------|
| Chunks indexed | 386 | 176 | 85 |
| Hit@4 | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Purity (on-target chunks) | 55/60 (92%) | 55/60 (92%) | **54/60 (90%)** |
| Mean first-hit rank | 1.13 | 1.07 | **1.00** |
| Worst first-hit rank | 3 | 2 | **1** |

(Hit@4 is structurally saturated on this corpus and is ignored — see the
[expanded-set artifact](2026-07-18-expanded-set.md).)

## The three weak questions

| Q | Target | 256/40 | 512/80 | 1024/160 |
|---|--------|--------|--------|----------|
| Q3 — "two dominant patterns for context construction" | Ch6 | rank 3, 2/4 (Ch5,Ch5,Ch6,Ch6) | rank 1, 2/4 (Ch6,Ch5,Ch5,Ch6) | rank 1, 1/4 (Ch6,Ch5,Ch5,Ch5) |
| Q8 — "where in a long input…" (Ch5/Ch6 trap) | Ch5 | rank 1, 2/4 (Ch5,Ch6,Ch5,Ch6) | rank 2, 2/4 (Ch6,Ch5,Ch5,Ch6) | rank 1, 1/4 (Ch5,Ch6,Ch6,Ch6) |
| Q13 — query rewriting (Ch4 leak) | Ch6 | rank 1, 3/4 (Ch6,Ch6,Ch6,Ch4) | rank 1, 3/4 (Ch6,Ch4,Ch6,Ch6) | rank 1, **4/4** (clean) |

## Observations

- **Chunk size redistributes the cross-chapter confusion; it does not remove
  it.** In all three configs, Q3 and Q8 still pull Ch5/Ch6 off-target chunks
  into the top-4. Smaller chunks trade Q8's rank for Q3's; larger chunks fix
  every rank but let more off-target chunks in. The failure mode — shared
  vocabulary across chapters — is invariant to chunk geometry.
- **256/40 is strictly not better**: identical purity (55/60), worse mean rank
  (1.13), and it produced the sweep's worst single result (Q3 at rank 3).
  More, smaller chunks fragment the distinctive passages without separating
  the confusable vocabulary.
- **1024/160 perfects rank but dilutes purity.** All 15 first hits at rank 1
  (mean 1.00) and Q13's Ch4 leak disappears (4/4). But Q3 and Q8 drop to 1/4
  purity (54/60 aggregate).
- **Purity fractions are not apples-to-apples across chunk sizes.** Q8 at
  512/80 retrieves 2×512 = ~1024 on-target tokens; at 1024/160 it retrieves
  1×1024 = ~1024 on-target tokens — the same evidence, inside a context twice
  as large (2048 → 4096 tokens). The fraction is still the right lens for
  generation: it measures signal concentration per context token, and doubling
  context also roughly doubles per-answer chat cost.
- **Verdict: no config wins — keep 512/80.** 1024/160's rank sweep is real but
  buys one cleaned cell (Q13) at the price of context dilution and 2× chat
  cost per answer; 256/40 loses outright. The Q3/Q8 confusion needs a
  retrieval-side fix that can *discriminate* between confusable chapters —
  hybrid (lexical + dense) retrieval or a reranker — which is exactly the next
  roadmap item. Those features should be judged on the same two metrics, with
  512/80 as the fixed baseline.

## Cost

Two fresh index builds + three 15-question eval runs ≈ **$0.004** total
(~190k embedded tokens) — see `docs/costs.md`.
