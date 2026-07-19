# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `docs/showcase/eval/2026-07-19-chunking-comparison.md` (the chunking null result and why the fix must be retrieval-side)

Now start the next measured feature iteration — **hybrid retrieval (dense + lexical)**, roadmap item 3 of ADR 005 continued.

Context: the chunking sweep proved chunk geometry can't fix the Ch5/Ch6 vocabulary confusion — Q3 and Q8 keep off-target chunks in the top-4 at every chunk size. The hypothesis for hybrid: lexical scoring (BM25-style) discriminates between chapters that share vocabulary better than embeddings alone, because the *distinctive* terms of the target passage get weighted up. Baseline to beat (512/80, dense top-4): purity 55/60 (92%), mean first-hit rank 1.07, worst 2; weak questions Q3 (2/4), Q8 (2/4, rank 2), Q13 (3/4).

Goals:

- add a lexical retrieval path over the existing 176-chunk corpus and fuse it with dense scores (simplest workable fusion first — e.g. reciprocal rank fusion; justify the choice in one line)
- keep `search_chunks`'s dense path intact and the hybrid path opt-in, so eval can run both sides against the same collection
- run `scripts.run_starter_eval` for dense (control) and hybrid with `--out docs/showcase/eval/2026-MM-DD-hybrid-<variant>.md`; the runner's Summary block makes runs one-glance comparable
- judge on purity and first-hit rank for Q3/Q8/Q13 (hit@4 reads 100% regardless); write the comparison artifact + update the showcase README log and case-study timeline; record the decision if hybrid wins
- add unit tests for the fusion logic (pure function, no API)

Requirements:

- plan first: show the design (lexical index location — in-memory vs Qdrant sparse vectors — fusion method, API changes) before touching anything; prefer the simplest option that avoids re-indexing
- stop Streamlit first (embedded Qdrant single-process lock); share one client
- lexical side is local and free; embedding calls only for eval queries — no chat API
- append API usage to `docs/costs.md`
- state the verification checks up front (pytest + eval tables as evidence)
- end with /handoff
