# Working-with-Claude learnings

Distilled from `my-rag-project` (Apr–Jul 2026): a solo learning-first RAG
project that evolved a session workflow, a layered knowledge architecture, and
a guardrail harness around Claude Code. Written to be portable — copy this
folder anywhere; nothing depends on the source repo.

| Doc | What it covers |
|-----|----------------|
| [01-session-workflow.md](01-session-workflow.md) | The session lifecycle: cold-start prompt → plan gate → work → artifact → handoff → checkpoint. How it emerged, and how it failed once. |
| [02-knowledge-architecture.md](02-knowledge-architecture.md) | The file layers that give an amnesiac assistant continuity: CLAUDE.md tiers, auto-memory, state files, ADRs, checkpoints, skills. Each fact lives in exactly one layer. |
| [03-guardrails.md](03-guardrails.md) | The harness: secrets handling, scope fences, eval gates, untrusted-input rules, testing and cost discipline. |

The one-sentence version: **treat every session as if it starts cold, ends
abruptly, and must leave the repo more navigable than it found it — because
all three are true.**
