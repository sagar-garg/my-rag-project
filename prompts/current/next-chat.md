# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `docs/showcase/eval/2026-07-18-baseline.md` (the baseline artifact — especially Observations)

Now expand the starter eval set — roadmap item 2 of ADR 005.

Context: the baseline is saturated (4/4 hit@4, all rank 1), so the current 4 questions cannot show improvement from any feature. The goal is a ~12–15 question set hard enough to produce real misses.

Goals:

- extend `data/eval/chapters_4_6_starter.json` to ~12–15 questions targeting Chapters 4–6
- make the new questions genuinely hard for dense retrieval:
  - no chapter names or numbers in the question wording
  - paraphrase concepts instead of quoting the chapters' own vocabulary
  - deliberately mine the Ch5/Ch6 vocabulary overlap (baseline Q3 pulled 2 Ch5 chunks for a Ch6 "context construction" question — that seam is where misses live)
  - a few multi-hop or cross-chapter questions (`target_sources` supports multiple files)
- re-run `.venv/bin/python -m scripts.run_starter_eval --out docs/showcase/eval/2026-MM-DD-expanded-set.md` and compare with the baseline
- update the artifact log in `docs/showcase/README.md` and the timeline in `docs/showcase/case-study.md`

Requirements:

- give a short plan first; I want to review the draft questions before they're saved (writing good eval questions is the judgment part — that's mine)
- remember the local embedded Qdrant single-process lock: stop Streamlit first; the eval script and `search_chunks` now share one client
- no chat-API calls needed — this stays retrieval-only
- end with /handoff
