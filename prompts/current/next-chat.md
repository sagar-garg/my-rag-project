# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `prompts/current/backlog.md`

Now build the baseline evaluation runner — the first roadmap item of ADR 005.

Goals:

- a script (suggest `scripts/run_starter_eval.py`) that loads the starter eval cases, runs retrieval only (no generation — keep the first pass free of chat-API cost), and reports per-question whether the retrieved chunks come from the expected chapter
- print a compact hit/miss table and write it as the first artifact to `docs/showcase/eval/2026-MM-DD-baseline.md`
- update the artifact log in `docs/showcase/README.md` and the timeline table in `docs/showcase/case-study.md`

Requirements:

- give a short plan first
- remember the local embedded Qdrant single-process lock: stop Streamlit first
- teach me briefly at important decisions; prefer small, reversible changes
- end with /handoff so state files stay current
