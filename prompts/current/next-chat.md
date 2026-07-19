# Next Chat Prompt

Read `CLAUDE.md`, then:

- `prompts/current/project-state.md`
- `docs/showcase/case-study.md` (the living draft — this session's raw material)
- `docs/showcase/README.md` (artifact log: 14 eval artifacts + 4 UI assets, all dated)

Now start **case-study assembly — roadmap item 5 of ADR 005**, the final item. Everything upstream is done: three measured retrieval iterations (null, negative, split) plus the gpt-5-mini coda, and a demo-ready UI with screenshots/GIF in `docs/showcase/assets/`. This session turns raw material into the publishable write-up.

Goals:

- **Architecture diagram**: mermaid source in the repo, exported SVG in `docs/showcase/assets/` (base it on the flowchart in `CLAUDE.md`/`README.md`; keep it stage-labeled: ingest → chunk → index → retrieve → generate, with eval alongside).
- **Fill the case-study TODOs**: "Learnings worth publishing" (distill from `docs/checkpoints/` and project-state's learnings list — pick the ~6 with general applicability, e.g. "a metric that can't fail measures nothing", "negative results compound", "the judge model is a hyperparameter") and tighten "The pitch".
- **Narrative pass**: the spine is measured iteration — baseline saturation → metric redesign → three mechanisms → content-ambiguity ceiling → the visible UI. Embed the assets (Q8 dense vs rerank screenshots are the money shots).
- **Export decision** (ask Sagar): target format for the personal website — plain markdown page, or something richer. Don't build site tooling unprompted.

Requirements:

- This is a writing/diagram session — no retrieval or UI logic changes; pytest stays green (42 tests) untouched.
- Verification: the deliverable is reviewable prose + a rendered diagram; show the diagram rendered (screenshot or SVG) rather than asserting it renders.
- Deposit anything new in `docs/showcase/` per the artifact habit.
- End with /handoff.

Parked (explicitly not this session unless Sagar redirects): Ragas generation-side metrics — **gated on the Azure migration** (chat deployment `gpt-4o` retires 2026-10-01; migrate to gpt-5.1 first so the metric series stays comparable — see backlog).
