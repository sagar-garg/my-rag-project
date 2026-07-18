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

**Total to date: well under one cent** (excluding any manual Streamlit chat
queries, which were not tracked — each is roughly fractions of a cent on a
mini-tier deployment).

## Projections

- Chunking sweep (next session): 2 extra index builds + 2 eval runs ≈ **+$0.004**.
- The first meaningful cost driver on the roadmap is **Ragas LLM-judge metrics**
  (faithfulness, answer relevancy): one chat call per question per metric per
  run. Estimate before running at scale.
