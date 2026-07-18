# Cursor-era configuration (archived)

These files were the project's AI-assistant configuration when it was used with Cursor. They are preserved for historical context only and are **no longer active**.

Superseded on **2026-04-19** by the Claude-native setup:

- Personal working philosophy lives in `~/.claude/CLAUDE.md` (applies to every project).
- Reusable workflows are skills in `~/.claude/skills/`: `handoff`, `secrets-handling`, `teach`, `record`.
- Project-specific context lives in the repo's top-level `CLAUDE.md`.

## What's here

- `rules/` — the original six `.cursor/rules/*.mdc` files (`project-defaults`, `python-style`, `python-teaching`, `learning-first-rag`, `prompt-workflow`, `secrets-handling`).
- `working-with-cursor.md` — the prior human-readable collaboration guide.

## Where the content went

| Old file | New home |
| --- | --- |
| `project-defaults.mdc` + `python-style.mdc` | Project `CLAUDE.md` (Python conventions + defaults) |
| `learning-first-rag.mdc` | Split: "what to avoid" list into project `CLAUDE.md`; teaching pattern into global `teach` skill |
| `python-teaching.mdc` | Global `teach` skill |
| `prompt-workflow.mdc` | Global `handoff` skill |
| `secrets-handling.mdc` | Global `secrets-handling` skill |
| `working-with-cursor.md` | Replaced by project `CLAUDE.md` + global philosophy |

Do not edit the files in this archive — if something needs updating, update the Claude-native equivalent.
