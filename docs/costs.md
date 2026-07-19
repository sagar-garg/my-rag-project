# Azure cost ledger

Running estimate of Azure OpenAI spend for this project. Update at the end of
any session that makes API calls (embedding or chat). Local Qdrant, Streamlit,
and pytest cost nothing.

## Price sheet (Azure OpenAI, as of 2026-07)

| Operation | Unit price | Notes |
|-----------|-----------|-------|
| Embeddings (`text-embedding-3-small-2`) | $0.02 / 1M tokens | the only cost in the retrieval-only workflow |
| Chat (Responses API) | depends on deployment | only used by Streamlit answers and future Ragas LLM-judge metrics — not by index builds or `run_starter_eval` |

## Per-operation cost model

| Operation | Tokens (est.) | Cost (est.) |
|-----------|---------------|-------------|
| Full index build (176 chunks × ≤512 tokens) | ~90k | **~$0.002** |
| One eval run (`run_starter_eval`, 15 questions) | ~0.5k | ~$0.00001 |
| One Streamlit question | ~30 embed + one chat call | embed negligible; chat call is the real cost (model/token dependent) |

## Ledger

Estimates, not invoices — reconstructed for pre-ledger entries. Verify against
the Azure portal (Cost Management) if precision ever matters.

| Date | Activity | Est. cost | Cumulative |
|------|----------|-----------|------------|
| 2026-04 | Initial builds: smoke corpus + chapters 4–6 (~2 full builds) | ~$0.004 | $0.004 |
| 2026-07-18 | Baseline eval (4 query embeds) | <$0.0001 | $0.004 |
| 2026-07-18 | Expanded eval (15 query embeds) | <$0.0001 | $0.004 |
| 2026-07-19 | Chunking sweep: 2 index builds (386 + 85 chunks ≈ 190k tokens) + 3 eval runs (45 query embeds) | ~$0.004 | $0.008 |
| 2026-07-19 | Hybrid iteration: 2 eval runs (30 query embeds ≈ 1k tokens); BM25 + RRF local, no index build | ~$0.00002 | $0.008 |
| 2026-07-19 | Rerank iteration: 2 LLM rerank runs on `gpt-4o` (165,880 in + 1,114 out tokens, actuals from API usage) + dense control + 2 diagnostic embeds | ~$0.43 | $0.44 |
| 2026-07-19 | Judge routing smoke test: 1 rerank call on `gpt-5-mini` (5,549 in + 993 out, ~960 of them reasoning tokens) | ~$0.003 | $0.44 |

**Total to date: ~$0.44**, almost all of it the 2026-07-19 rerank iteration —
the chat deployment turned out to be full-size `gpt-4o` (~$2.50/1M input), not
a mini tier, so each 15-question rerank run costs ~$0.21. Retrieval-only
(dense/hybrid) evals remain effectively free. Manual Streamlit chat queries
are still untracked.

## Projections

- ~~Chunking sweep~~ — done 2026-07-19, landed on the estimate (+$0.004).
- ~~Hybrid retrieval~~ — done 2026-07-19 at ~zero cost as predicted (rejected
  on eval evidence; dense stays).
- ~~LLM reranker~~ — done 2026-07-19 (+$0.43 for two runs on `gpt-4o`; split
  decision, stays opt-in). Lesson: check which deployment
  `AZURE_OPENAI_CHAT_DEPLOYMENT` points at before estimating — mini-tier vs
  full gpt-4o is a ~15× price difference. A mini deployment would make rerank
  runs ~$0.015.
- The next cost driver on the roadmap is **Ragas LLM-judge metrics**
  (faithfulness, answer relevancy): one chat call per question per metric per
  run on the same `gpt-4o` deployment — estimate (and consider a mini
  deployment) before running at scale.
