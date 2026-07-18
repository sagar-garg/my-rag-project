# The session workflow: handoff, record, and moving each session along

## The core insight

Chat sessions are ephemeral; the repo is permanent. Any knowledge that exists
only in a conversation is already lost — you just don't know it yet. So the
workflow's job is to make every session **resumable by a stranger** (which
includes future-you and the next Claude session, both of whom start cold).

## The lifecycle

```
next-chat.md  ──►  plan gate  ──►  work  ──►  artifact  ──►  /handoff  ──►  /clear
 (cold start)      (review before    │        (measured       │
                    files change)    │         evidence)      ├── project-state.md   (what's true now)
                                     │                        ├── next-chat.md       (the next session's opening prompt)
                                     │                        ├── backlog.md         (what's queued, re-prioritized)
                                     │                        └── checkpoint / ADR   (if a milestone or decision landed)
                                     └── tests + commit under the right identity
```

- **`next-chat.md`** holds exactly one prompt: the single best way to open the
  next session. Self-contained — it names the files to read first, the goal,
  and the constraints (e.g. "stop Streamlit first", "no chat API", "plan
  first"). One prompt, not a menu: it kills decision fatigue at session start.
- **The plan gate** is a hard rule, not a vibe: non-trivial work → show the
  plan, wait for approval, don't touch files. Crucially, the gate marks where
  *judgment* lives. When the task was writing eval questions, the prompt said
  it explicitly: "I review the draft questions before they're saved — writing
  good eval questions is the judgment part; that's mine." The assistant
  compresses the legwork; the human keeps the decisions.
- **The artifact habit**: if a session produces a measurable result and no
  artifact lands in the showcase folder, the session isn't finished. Collecting
  evidence at milestone time is cheap; reconstructing it months later is
  expensive or impossible (screenshots of intermediate states, most of all).
- **`/handoff`** (a custom skill) closes the loop: summarize the session for
  correction *before* writing it into files, then update the three state files,
  update durable learnings in docs, and checkpoint if a milestone was reached.
- **`/record`** (a custom skill) scaffolds the two durable artifact types:
  **ADRs** ("why we chose X over Y") and **checkpoints** ("what works as of
  date Z"). Both are written for a reader with zero context, six months out.

## How this system emerged (three stages, each forced by a failure)

1. **v1: one master prompt file.** The project began (Cursor era) with a
   single `prompts/v1.md` holding the full end-to-end prompt sequence. Real
   implementation immediately diverged from it — order changed, learnings
   accumulated, the file went stale. Lesson: *a prompt sequence is a plan, and
   plans rot; don't let them masquerade as the source of truth.*
2. **ADR 003: the split.** The fix separated concerns by shelf life:
   `docs/` for durable truth, `prompts/current/` for the moving frontier
   (state / next prompt / backlog), `prompts/archive/` for frozen history,
   `docs/checkpoints/` for milestone snapshots. Checkpoints beat chat
   transcripts: scannable, dated, factual.
3. **ADR 005: the stress test.** The system then failed in the one way it
   couldn't self-detect: three months of real work (a vector-store migration,
   a tooling migration) sat **uncommitted in a side worktree**. The handoff
   files described a world that git didn't contain; the gap was only
   reconstructible from a diff. Lesson: *the handoff system's substrate is
   git — uncommitted work silently defeats all of it. Commit at session end,
   every session.* The repair also added the artifact habit and consolidated
   to a single branch — a solo project with serial milestones gains nothing
   from parallel worktrees except this exact failure mode.

## Learnings worth carrying to any project

- **End-of-session writing is the highest-leverage 10 minutes.** The handoff
  files convert a conversation into repo state. Skip it once and the next
  session pays double.
- **One next-prompt beats a backlog at session start.** The backlog exists,
  but the cold-start file contains a single, fully-formed prompt. Choosing is
  the previous session's job, when context is loaded.
- **Milestone snapshots > session logs.** Checkpoints record *what works*,
  verified, with the corpus/config it was verified against — not what was
  attempted. "Facts, not marketing" is in the skill's rules.
- **Frozen history is a feature.** Archived prompts are never rewritten. You
  can see what v1-you believed, which is how the origin story in this doc was
  reconstructible at all.
- **A summary shown before it's saved is a correction opportunity.** The
  handoff skill summarizes the session to the human *first*, then writes.
- **Findings are outcomes.** A 100% baseline that can't show improvement was
  recorded as a finding that redirected the roadmap — not padded into a
  success. The workflow makes negative results durable, which is what makes
  the eval-gated roadmap honest.
- **Sessions end with `/clear`, guilt-free.** When the workflow works, the
  conversation is disposable by design. "Is this chat ready to clear?" has a
  checkable answer: handoff done, artifacts deposited, commit made.
