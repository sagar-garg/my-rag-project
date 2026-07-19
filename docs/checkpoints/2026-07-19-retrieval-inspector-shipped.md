# Retrieval inspector UI shipped; gpt-5-mini rerank coda measured

## Date
2026-07-19 (evening — same day as the reranking checkpoint; separate milestone)

## Outcome
ADR 005 roadmap item 4 (UI polish) is done. The Streamlit app now demos the whole measured-iteration story live: a sidebar retrieval-mode toggle (dense / hybrid / LLM rerank, cost-labeled) and a retrieval inspector that shows per-chunk chapter, index, and score with expected-vs-actual ✅/❌ highlighting whenever the typed question matches the 15-question eval set. The first showcase assets exist — three screenshots and a mode-toggle GIF captured from the live app. Earlier the same session, the gpt-5-mini rerank coda (two full runs) narrowed but did not flip the rerank verdict: first-hit rank saturated at 1.00 in both runs with no regressions at ~¼ gpt-4o's cost, purity stayed a 55/60 wash, so dense top-4 remains the default.

## What works
- Streamlit UI with dense / hybrid / rerank retrieval modes, one shared embedded-Qdrant client (`st.cache_resource`), BM25 index session-cached per collection, rerank token-usage readout on the `gpt-5-mini` judge.
- Retrieval inspector: eval-question matching (`app/ui/inspector.py::find_matching_case`), hit/rank/purity banner via the existing `judge_retrieval`, per-chunk on-target highlighting; verified live on Q1 (clean 4/4) and Q8 (the Ch5/Ch6 trap at rank 2 dense, rank 1 rerank).
- `docs/showcase/assets/`: clean-hit, Q8-dense, Q8-rerank screenshots + 4-frame demo GIF; logged in the showcase README and case study.
- 42 pytest tests green (34 prior + 8 for the new pure helpers).
- Eval artifacts for the coda: two gpt-5-mini rerank runs + comparison doc (`docs/showcase/eval/2026-07-19-rerank-gpt5mini-*.md`); cost ledger at ~$0.54 total.

## Corpus / data / inputs used
Chapters 4–6 corpus (`book_chapters_4_6`, 512/80, 176 chunks); 15-question starter eval set; live driving of the app via Playwright at 1440px.

## Important lessons
- The judge model is a hyperparameter: same rerank prompt, gpt-4o → gpt-5-mini, and first-hit rank saturates (1.00 both runs, no regressions) at ¼ the cost. And an n=1 smoke test misleads — its perfect Q8 purity didn't survive two full runs.
- A saturated metric can be retired: rank has joined hit@4; purity is the only discriminating metric left on this corpus.
- Streamlit reruns overlap briefly (cooperative cancellation), so a one-instance-per-process resource like the embedded Qdrant client must be shared via `st.cache_resource` — per-rerun creation races intermittently (first click failed, second succeeded, which is the signature).
- Driving the real app finds bugs tests don't: the lock race and a `$`-triggers-LaTeX rendering bug both surfaced only in the browser.

## Next step
Case-study assembly (roadmap item 5, the last): architecture diagram, narrative from the artifact log, export for the personal website. See `prompts/current/next-chat.md`.
