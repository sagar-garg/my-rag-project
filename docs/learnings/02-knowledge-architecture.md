# Knowledge architecture: the file layers that steer Claude

## The problem being solved

The assistant starts every session with amnesia, and its instruction-following
degrades as instructions bloat. The answer is not "write everything down
everywhere" — it's a layered architecture where **each fact lives in exactly
one layer**, chosen by shelf life and scope, with explicit budgets and a
linting habit to keep the layers from rotting.

## The layers, from most global to most ephemeral

| Layer | Scope | Shelf life | Contains |
|-------|-------|-----------|----------|
| Global `~/.claude/CLAUDE.md` | every project | years | how I work: operating mode, push-back norms, effort calibration, output style. **Not** project facts. |
| Project `CLAUDE.md` | one repo | months | the repo's WHAT/WHY/HOW: stack, module map, conventions, workflow pointers, scope fences. Explicitly "adds only what's specific to this project". |
| Auto-memory | one repo, cross-session | months | facts not derivable from the repo: who the user is, environment quirks (e.g. "vector store is local embedded; cloud cluster deleted"). One fact per file, indexed in MEMORY.md. |
| `prompts/current/` | one repo | weeks | the moving frontier: project-state, next-chat, backlog. Rewritten freely at each handoff. |
| `docs/decisions/` (ADRs) | one repo | permanent | why X over Y, with alternatives and accepted tradeoffs. Append-only as a set; individual ADRs get superseded, never edited into lies. |
| `docs/checkpoints/` | one repo | permanent | dated "what works" snapshots with lessons. Append-only. |
| `docs/showcase/` | one repo | permanent | evidence: eval tables, screenshots, the living case-study draft. |
| Skills (`~/.claude/skills/`) | every project | years | *procedures*, not facts: handoff, record, secrets-handling, systematic-debugging, teach, lint-knowledge. |
| The conversation | one session | hours | everything else. Disposable by design. |

## Principles that make the layers work

- **Route by shelf life.** "Still true next month?" → docs. "True until the
  next session?" → prompts/current. "True only today?" → nowhere, let it die
  with the chat. The handoff skill encodes this question explicitly.
- **Don't duplicate across layers.** Memory doesn't store what the repo
  records (code structure, git history, CLAUDE.md content). Rules appearing in
  two CLAUDE.md tiers: keep the more specific one, delete the other.
- **Budgets are real.** Global CLAUDE.md under ~60 lines, project under ~150.
  Past the budget, instructions stop being followed reliably — trimming is
  maintenance, not loss.
- **Procedures become skills, not prose.** A rule you must *follow* ("at
  session end, update these three files, in this way, then maybe checkpoint")
  works far better as an invocable skill with steps than as a paragraph the
  model may or may not recall. The project's whole workflow is skill-shaped:
  `/handoff`, `/record`, `/secrets-handling`, `/lint-knowledge`, `/teach`.
- **Skills carry their own trigger conditions.** Each skill's description says
  *when* it applies ("use when the user says wrap up / end of chat…"), so
  invocation doesn't depend on remembering the skill exists.
- **Knowledge needs linting like code does.** A dedicated skill
  (`lint-knowledge`) health-checks the markdown layer on a cadence: stale
  facts vs. the filesystem, contradictions between layers, broken index
  entries, budget overruns. Report first, fix only after approval. Docs rot
  silently; scheduled linting is the only real countermeasure.
- **Teaching is opt-in.** A `teach` skill exists but fires only when asked —
  "unprompted teaching is noise." The default is compression, not lecturing.
- **Config migrations preserve history.** When tooling moved (Cursor → Claude
  Code), old rules were archived (`docs/archive/cursor/`), not deleted — same
  frozen-history principle as prompt archives.

## What made this architecture earn its keep

- Session N+1 opens with two file reads and is fully oriented — including
  after a three-month gap. That's the test: **could a stranger resume this
  project from the files alone?**
- The layered split kept the project CLAUDE.md short enough to actually be
  followed, because state, history, and rationale each had somewhere else
  to live.
- ADRs turned "why is it built this way?" from an unanswerable question into
  a file read — including for decisions that would otherwise look wrong
  (e.g. "why is the vector store local? because the cloud cluster was deleted;
  it's in memory *and* ADR 002").
