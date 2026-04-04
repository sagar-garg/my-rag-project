# Decision 003: Prompt and checkpoint workflow

## Status
Accepted

## Context

The original `prompts/v1.md` contained a full end-to-end sequence for the project, but real implementation changed the order, added integration learnings, and made parts of that sequence stale. We need a workflow that preserves history without letting prompts become the project's main source of truth.

## Decision

Use this split:

- `docs/` for durable project truth
- `prompts/archive/` for retired prompt sets
- `prompts/current/project-state.md` for current state
- `prompts/current/next-chat.md` for the single best next prompt
- `prompts/current/backlog.md` for future tasks
- `prompts/templates/` for reusable prompt shapes
- `docs/checkpoints/` for milestone snapshots

## Why

- Project docs should capture facts and durable lessons.
- Prompt files should stay focused on workflow and next actions.
- Checkpoints are easier to scan later than long chat transcripts or stale prompt sequences.
- A single `next-chat.md` reduces decision fatigue at the start of the next session.

## Alternatives considered

- Keep one evolving master prompt file:
  Rejected because it becomes a confusing mix of history, plan, and current state.
- Put all workflow guidance only in rules:
  Rejected because the guidance should remain easy to inspect and update from inside the repo.

## Consequences

- At the end of substantial chats, both docs and prompt workflow files should be updated.
- Archived prompt files should remain frozen.
- The next session should usually start from `prompts/current/next-chat.md`, not from an old prompt archive.
