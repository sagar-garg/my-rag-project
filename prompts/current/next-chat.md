# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `prompts/current/backlog.md`
- `docs/costs.md` (cost ledger — pricing entries will need updating)

**The ADR 005 roadmap is complete** (case study assembled 2026-07-19; export decision: markdown as-is — website adaptation happens in the website repo, not here). The next project step is the **Azure model migration**, which gates the Ragas generation metrics: `AZURE_OPENAI_CHAT_DEPLOYMENT` is `gpt-4o`, deprecated on Azure and retiring 2026-10-01; a mid-series model swap would break metric comparability, so migrate first, measure after.

Goals:

- Switch the chat deployment to `gpt-5.1`: create the deployment on the existing Azure resource (Sagar may need to do the portal step — ask him to run it if CLI access is missing) and update `AZURE_OPENAI_CHAT_DEPLOYMENT`. The judge deployment stays `gpt-5-mini`.
- Confirm nothing regresses: pytest green (42), one real grounded answer generated through `generation.respond` or the Streamlit app, and a dense eval control run (retrieval is embedding-side, so expect byte-identical results: purity 55/60, mean rank 1.07, worst 2 — any deviation is a red flag, not noise).
- Update `docs/costs.md` with gpt-5.1 pricing; note any Responses API surprises (the Responses API needs `2025-03-01-preview` or later — verify the new model doesn't need a newer version).
- If the migration completes cleanly with time left: start the **first Ragas generation baseline** (faithfulness, answer relevancy) on the 15-question set, judge calls routed to `gpt-5-mini` — this opens the post-migration metric series and is the natural next measured iteration.

Requirements:

- Verification stated up front (drill): the checks are pytest output, the dense-control eval artifact matching the known baseline, and a shown generated answer — evidence, not assertion.
- Any eval run deposits its artifact in `docs/showcase/eval/` per the artifact habit.
- End with /handoff.

Parked: website integration of the case study (belongs to the website repo); rerank `reasoning={"effort": "low"}` knob (only if rerank mode gets interactive use).
