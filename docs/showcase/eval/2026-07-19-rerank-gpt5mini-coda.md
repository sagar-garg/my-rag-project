# Rerank coda: gpt-5-mini as judge — rank metric saturates, purity verdict stands — 2026-07-19

Coda to [the gpt-4o rerank comparison](2026-07-19-rerank-comparison.md). After
judge-call routing landed (`AZURE_OPENAI_JUDGE_DEPLOYMENT=gpt-5-mini`), a
single Q8 smoke test scored a perfect 4/4 rank-1 — enough to justify rerunning
the full eval on the cheaper judge. Same setup as the gpt-4o runs: dense
top-12 candidates, one listwise rerank call per question, top-4 kept, 15
questions, **two runs** (nondeterministic component). Per-run artifacts:
[run 1](2026-07-19-rerank-gpt5mini-run1.md) ·
[run 2](2026-07-19-rerank-gpt5mini-run2.md).

## Aggregate results

| Metric | Dense (control) | gpt-4o rerank (runs 1–2) | gpt-5-mini rerank run 1 | gpt-5-mini rerank run 2 |
|--------|-----------------|--------------------------|-------------------------|-------------------------|
| Hit@4 | 15/15 | 15/15 | 15/15 | 15/15 |
| Purity | **55/60 (92%)** | 56/60 · 55/60 | 55/60 (92%) | 55/60 (92%) |
| Mean first-hit rank | 1.07 | 1.07 · 1.07 | **1.00** | **1.00** |
| Worst first-hit rank | 2 (Q8) | 2 (Q5) · 2 (Q5) | **1** | **1** |
| Cost / run | ~$0.0001 | ~$0.21 | ~$0.05 | ~$0.05 |

## The questions that moved

| Q | Target | Dense | gpt-4o (stable outcome) | gpt-5-mini run 1 | gpt-5-mini run 2 | Stable? |
|---|--------|-------|-------------------------|------------------|------------------|---------|
| Q3 — context-construction patterns | Ch6 | r1, 2/4 | r1, 4/4 (gain) | r1, 4/4 | r1, 3/4 | gain, ±1 jitter |
| Q5 — "did the model make something up" | Ch4 | r1, 4/4 | **r2**, 3/4 (regression) | r1, 2/4 | r1, 2/4 | ❌ purity regression stable; rank recovered |
| Q8 — long-input position (Ch5/Ch6 trap) | Ch5 | **r2**, 2/4 | r1, 2–3/4 | r1, 2/4 | r1, 3/4 | ✅ rank fix stable; purity jitters — smoke test's 4/4 did **not** replicate |
| Q9 — Santa / tone paraphrase | Ch5 | r1, 4/4 | 3–4/4 jitter | r1, 3/4 | r1, 3/4 | −1 purity, stable here |
| Q13 — query rewriting (Ch4 leak) | Ch6 | r1, 3/4 | 2–3/4 jitter | r1, 4/4 | r1, 4/4 | ✅ stable gain |

## Observations

- **The rank metric saturates under gpt-5-mini.** All 15 questions at
  first-hit rank 1, in both runs — dense never managed it (worst 2) and
  gpt-4o's rerank traded Q8's fix for a Q5 rank regression. gpt-5-mini makes
  no rank mistakes at all. As with hit@4 before it, a saturated metric stops
  discriminating: first-hit rank now joins hit@4 as a solved dimension on
  this corpus, leaving purity as the only metric with headroom.
- **Purity is a wash — the same 55/60, redistributed.** gpt-5-mini fixes
  dense's impure questions (Q13 fully, Q3/Q8 partially) but pays for it on
  Q5 (stably 2/4, worse than gpt-4o's 3/4) and Q9 (stably 3/4). The
  candidate-pool double-edge from the gpt-4o analysis is unchanged: the
  wider pool that lets the reranker fix Q8 exposes plausible off-target
  text on questions dense had clean.
- **The pre-registered flip criteria were not met** (Q5 not regressed;
  aggregate > dense). The smoke test's perfect Q8 was an n=1 fluke — across
  two full runs Q8's purity is 2–3/4, same band as gpt-4o. One more point
  for the repeat-runs rule: a single call proved the routing worked, but
  only the full runs could say what the judge actually does.
- **gpt-5-mini strictly dominates gpt-4o as the rerank judge**: equal or
  better on every metric (rank: better; purity: equal aggregate; no rank
  regressions) at ~¼ the cost (~$0.05 vs ~$0.21 per run). Whatever the
  reranker's future here, gpt-4o should never judge again. Reasoning tokens
  are the cost driver: ~14.7k output tokens/run (~1k per call, mostly
  reasoning) vs gpt-4o's ~0.6k — `reasoning={"effort": "low"}` is the
  untested knob if latency ever matters.

## Verdict

**Dense top-4 stays the default; the split decision narrows but stands.**
Reranking with gpt-5-mini is now a clean win on first-hit rank (1.00, no
regressions) and a wash on purity — a better deal than gpt-4o's version, but
purity is the binding metric (rank was already 1.07 of a possible 1.00), and
+$0.003 and +1–2 s per query buys no purity. The residual ~8% impurity
remains content ambiguity, beyond any of the four mechanisms now measured
(geometry, lexical, gpt-4o reader, gpt-5-mini reader). `--mode rerank` stays
opt-in, now materially better and cheaper than when the split decision was
called.

## Cost

Two runs: 165,850 input + 29,414 output tokens on `gpt-5-mini`
(~$0.05/run, **~$0.10 total**); 30 query embeds negligible. See
`docs/costs.md`.
