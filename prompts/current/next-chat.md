# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `docs/showcase/eval/2026-07-19-rerank-comparison.md` (how retrieval-side iteration closed)
- `app/ui/streamlit_app.py` (current UI state)

Now start **UI polish — roadmap item 4 of ADR 005**, the first non-eval iteration.

Context: retrieval work is closed. Three measured mechanisms (chunk geometry, lexical/hybrid, LLM reranking) bounded the residual ~8% impurity as cross-chapter content ambiguity; dense top-4 stays the default, with `--mode hybrid` and `--mode rerank` in the eval runner as documented controls. The case study's spine — measured iteration with two nulls and a split decision — is complete. What's missing is the *visible* layer: a demo-ready UI and the screenshots/GIFs that `docs/showcase/assets/` is still empty of.

Goals:

- **Retrieval inspector in Streamlit**: per query show retrieved chunks with scores, source chapter, chunk index, and expected-vs-actual highlighting when the query matches an eval question (load `data/eval/chapters_4_6_starter.json` for targets). This is backlog's top medium-term item.
- Optional retrieval-mode toggle (dense / hybrid / rerank) in the UI sidebar — it makes the case-study demo show the measured comparison live. Note: rerank mode costs ~$0.014/query on the current full-size `gpt-4o` deployment; label it in the UI.
- **Capture showcase assets**: screenshots of the inspector on a clean hit and on Q8 (the famous trap), ideally a short demo GIF → `docs/showcase/assets/`, logged in `docs/showcase/README.md` and referenced from `case-study.md`.
- No retrieval-logic changes — the eval verdicts are settled; this session is presentation only.

Requirements:

- Embedded Qdrant single-process lock: the Streamlit app owns the store while running — don't run `build_index`/eval scripts concurrently.
- Verification checks, stated up front: pytest stays green (34 tests); UI verified by driving the running app and capturing the screenshots themselves (the assets are the evidence); no new dependencies without justification.
- Keep UI code in `app/ui/`; pure helper logic (eval-question matching, chapter labeling) goes where it's testable with at least one unit test.
- End with /handoff.
