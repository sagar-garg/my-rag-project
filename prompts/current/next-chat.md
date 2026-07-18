# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `docs/showcase/eval/2026-07-18-expanded-set.md` (especially Observations — the metric-shift finding)

Now start the first measured feature iteration — roadmap item 3 of ADR 005: **chunking parameters**.

Context: the eval set is 15 questions and hit@4 is structurally saturated (100% is unmissable at chapter level on a 3-file corpus). The gating metrics are now **purity** (55/60 = 92%) and **first-hit rank** (worst: 2). The weak questions are Q3 (2/4), Q8 (2/4, rank 2), Q13 (3/4) — all cross-chapter vocabulary confusion between Ch5/Ch6 (and one Ch4 leak).

Goals:

- sweep 2–3 chunking configurations against the current one (size 512 / overlap 80) — e.g. smaller (256/40) and larger (1024/160); each needs a fresh `QDRANT_COLLECTION_NAME` and a re-index
- run `scripts.run_starter_eval` per config with `--out docs/showcase/eval/2026-MM-DD-chunking-<size>.md --title "Chunking <size>/<overlap>"`
- compare on purity and first-hit rank per question (hit@4 will read 100% everywhere — ignore it); does any config clean up Q3/Q8/Q13 or push Q8 back to rank 1?
- consider extending the runner's summary output with aggregate purity and mean first-hit rank, so per-run tables are directly comparable
- update the artifact log in `docs/showcase/README.md` and the case-study timeline; if a config wins, record the decision

Requirements:

- plan first: show me the sweep matrix (configs, collection names, cost estimate — each re-index embeds the full corpus) before touching anything
- stop Streamlit first (embedded Qdrant single-process lock); share one client
- embedding calls only (re-index + 15 queries per config) — no chat API
- append the session's API usage to `docs/costs.md` (running Azure cost ledger)
- end with /handoff
