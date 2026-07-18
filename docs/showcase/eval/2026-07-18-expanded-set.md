# Expanded eval set (15 questions) — 2026-07-18

**Hit rate: 15/15 (100%)** — hit@4, retrieval only (no generation).

A question counts as a hit if any retrieved chunk comes from the expected chapter PDF. Rank is the position of the first on-target chunk (1 = best).

## Configuration

- Collection: `book_chapters_4_6` (local embedded Qdrant)
- Chunking: size 512, overlap 80
- Retrieval: dense top-4
- Embeddings: `text-embedding-3-small-2`

## Per-question results

| # | Question | Expected | Result | First-hit rank | On-target | Retrieved (by rank) |
|---|----------|----------|--------|----------------|-----------|---------------------|
| 1 | What does evaluation-driven development mean in the book? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 2 | Why should teams make the most of prompting before moving to finetuning? | Ch5 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 3 | What are the two dominant patterns for context construction described in Chapter 6? | Ch6 | ✅ hit | 1 | 2/4 | Ch6, Ch5, Ch5, Ch6 |
| 4 | According to Chapter 6, why does longer context not eliminate the need for RAG? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 5 | How can you tell whether a model made something up, without checking any external source? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 6 | Why can't I just pick whichever model tops the public leaderboards for my application? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 7 | How many examples do I need before I can trust that one system is really better than another? | Ch4 | ✅ hit | 1 | 4/4 | Ch4, Ch4, Ch4, Ch4 |
| 8 | Where in a long input should important information be placed so the model doesn't overlook it? | Ch5 | ✅ hit | 2 | 2/4 | Ch6, Ch5, Ch5, Ch6 |
| 9 | The bot keeps answering children's questions in a way that ruins the magic — how do I fix its tone without retraining it? | Ch5 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 10 | Someone got our assistant to reveal its hidden configuration text — how does that attack work and why does it matter? | Ch5 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch5 |
| 11 | Our search misses documents when users type exact product codes, though it works fine for descriptive queries — what's going on and what's the standard fix? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 12 | What are the downsides of splitting documents into very small pieces before indexing them? | Ch6 | ✅ hit | 1 | 4/4 | Ch6, Ch6, Ch6, Ch6 |
| 13 | Follow-up questions like 'what about her?' return junk results — what technique addresses this? | Ch6 | ✅ hit | 1 | 3/4 | Ch6, Ch4, Ch6, Ch6 |
| 14 | What new risks appear when an assistant can read web pages or files that strangers can edit? | Ch5, Ch6 | ✅ hit | 1 | 4/4 | Ch5, Ch5, Ch5, Ch6 |
| 15 | When a system that looks up documents before answering gives a bad answer, how do I figure out which part to blame? | Ch4, Ch6 | ✅ hit | 1 | 4/4 | Ch4, Ch6, Ch4, Ch4 |

## Observations

Set expanded 4 → 15 questions (originals kept verbatim as Q1–Q4; 11 new questions
avoid chapter names and chapter-title vocabulary, paraphrase concepts, and include
deliberate Ch5/Ch6 traps plus two cross-chapter questions).

- **Hit@4 stayed 15/15 — but that's now a structural ceiling, not a success.**
  With only 3 source PDFs and 4 retrieved chunks, a chapter-level "any chunk
  counts" hit is nearly impossible to miss: all 4 chunks would have to come from
  the two wrong chapters. This metric saturated at baseline and cannot
  un-saturate on this corpus. The discriminative signal has moved to **purity**
  (on-target fraction) and **first-hit rank**.
- **The traps drew blood on those finer metrics.** Q8 ("where in a long input…",
  the designed Ch5-vs-Ch6 trap) produced the set's first non-rank-1 result:
  first hit at rank 2, purity 2/4, with Ch6's long-context-vs-RAG chunks
  taking ranks 1 and 4 — exactly the confusion it was built to cause. Q13
  (query rewriting) leaked a Ch4 chunk at rank 2 (purity 3/4). Baseline Q3
  remains 2/4. Everything else stayed 4/4 at rank 1.
- **Headroom for feature work now exists, but in purity/rank, not hit rate:**
  overall purity 55/60 (92%), mean first-hit rank 1.07. Hybrid retrieval and
  reranking should be judged on whether they clean up Q3/Q8/Q13 purity and
  push Q8 back to rank 1 — hit@4 will read 100% → 100% regardless.
- **Surprise: paraphrase distance is not a hardness axis for this embedding
  model.** Q9 (the Santa question — zero shared vocabulary with its target
  passage, "ruins the magic" → fictional-characters example) came back a clean
  4/4 at rank 1. Semantic paraphrase is easy for `text-embedding-3-small`;
  what actually degrades it is *shared vocabulary across chapters* (Q8's "long
  input"). Future hard questions should exploit cross-chapter lexical overlap,
  not obliqueness.
- **If real misses are ever needed, the gold labels must get finer than the
  chapter.** Section-level or chunk-level targets (which passage answers the
  question) would let hit@k actually fail. Chapter-level judgment on a 3-file
  corpus is too coarse — worth doing only if purity/rank stop discriminating.

### Baseline comparison

| Metric | Baseline (4 q) | Expanded (15 q) |
|--------|----------------|-----------------|
| Hit@4 | 4/4 (100%) | 15/15 (100%) |
| Purity (on-target chunks) | 14/16 (88%) | 55/60 (92%) |
| Questions below 4/4 purity | 1 (Q3) | 3 (Q3, Q8, Q13) |
| Worst first-hit rank | 1 | 2 (Q8) |
