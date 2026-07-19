# LLM listwise rerank (dense top-12 → top-4) — 2026-07-19

**Hit rate: 15/15 (100%)** — hit@4, retrieval only (no generation).

A question counts as a hit if any retrieved chunk comes from the expected chapter PDF. Rank is the position of the first on-target chunk (1 = best).

## Configuration

- Collection: `book_chapters_4_6` (local embedded Qdrant)
- Chunking: size 512, overlap 80
- Retrieval: LLM rerank (gpt-4o) of dense top-12 → top-4
- Embeddings: `text-embedding-3-small-2`

## Summary

| Metric | Value |
|--------|-------|
| Hit@4 | 15/15 (100%) |
| Purity (on-target chunks) | 56/60 (93%) |
| Mean first-hit rank | 1.07 |
| Worst first-hit rank | 2 |

## Per-question results

| # | Question | Expected | Result | First-hit rank | On-target | Retrieved (by rank) |
|---|----------|----------|--------|----------------|-----------|---------------------|
| 1 | What does evaluation-driven development mean in the book? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 2 | Why should teams make the most of prompting before moving to finetuning? | Ch5 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 3 | What are the two dominant patterns for context construction described in Chapter 6? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 4 | According to Chapter 6, why does longer context not eliminate the need for RAG? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 5 | How can you tell whether a model made something up, without checking any external source? | Ch4 | ✅ hit | 2 | 3/4 | Ch5, Ch4, Ch4, Ch4 |
| 6 | Why can't I just pick whichever model tops the public leaderboards for my application? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 7 | How many examples do I need before I can trust that one system is really better than another? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 8 | Where in a long input should important information be placed so the model doesn't overlook it? | Ch5 | ✅ hit | 1 | 2/4 | Ch5, Ch5, Ch6, Ch6 |
| 9 | The bot keeps answering children's questions in a way that ruins the magic — how do I fix its tone without retraining it? | Ch5 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 10 | Someone got our assistant to reveal its hidden configuration text — how does that attack work and why does it matter? | Ch5 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 11 | Our search misses documents when users type exact product codes, though it works fine for descriptive queries — what's going on and what's the standard fix? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 12 | What are the downsides of splitting documents into very small pieces before indexing them? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 13 | Follow-up questions like 'what about her?' return junk results — what technique addresses this? | Ch6 | ✅ hit | 1 | 3/4 | Ch6, Ch6, Ch4, Ch6 |
| 14 | What new risks appear when an assistant can read web pages or files that strangers can edit? | Ch5, Ch6 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 15 | When a system that looks up documents before answering gives a bad answer, how do I figure out which part to blame? | Ch4, Ch6 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch6, Ch4 |

## Observations

_TODO: notes on misses and near-misses — this feeds the case study._
