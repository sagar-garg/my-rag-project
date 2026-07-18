# Guardrails: the harness around the assistant

The harness has three jobs: keep secrets out of the conversation, keep scope
from creeping, and keep claims honest. Each guardrail below exists because the
failure it prevents is cheap to cause and expensive to undo.

## Secrets

The rules live in two places: a repo doc (`docs/security-basics.md`, the
policy) and an enforcing skill (`secrets-handling`, the procedure). The split
matters — the doc states the baseline; the skill fires automatically whenever
a request involves `.env`, keys, or credentials, so enforcement doesn't depend
on anyone remembering the doc.

- Secrets live only in `.env`; `.env.example` is committed and documents
  the schema. **The assistant reads `.env.example`, never `.env`** — debugging
  almost always needs variable *names*, not values.
- Reading a secret file requires explicit approval **in that turn**; prior
  approvals don't carry over.
- Any secret that appears in chat, logs, code, or a screenshot is treated as
  exposed: rotate it. No partial-value quoting ("first 4 chars") either.
- Never `git add .env`; warn if a secret file is ever staged.
- When a live secret is genuinely needed (e.g. testing an API call), the
  *user* runs the command in their own terminal rather than the assistant
  reading the secret to pass it along.

## LLM-specific input handling (for RAG and agent systems)

- **Retrieved text is prompt input, not instructions.** System rules live in
  code; retrieved content goes only into the context slot; the grounding
  prompt explicitly tells the model not to follow instructions found inside
  documents. Always return citations. (This mirrors indirect prompt injection
  — the corpus's own Chapter 5 — where attackers plant instructions in
  content the system will retrieve.)
- Don't fetch arbitrary URLs from model output; don't auto-execute
  model-generated code; call only the endpoints you expect.

## Scope fences

- **An explicit "avoid unless requested" list** in CLAUDE.md (LiteLLM, MCP
  servers, DSPy, GraphRAG, multi-agent orchestration, JS frameworks, heavy
  observability). The escape hatch is built in: "if a problem seems to need
  one of these, first ask whether a simpler approach gets us 80% there."
- **The fence is versioned, not sacred.** When the project direction changed
  (ADR 005), hybrid retrieval and reranking were formally *removed* from the
  avoid list and became roadmap items — via a recorded decision, not silent
  drift. Scope changes leave a paper trail.
- **Eval-gated features:** nothing retrieval-related ships without a measured
  before/after against the eval set. The gate caught its own weakness too —
  when the metric saturated, the finding was recorded and the metric was
  changed rather than declaring victory.
- Justify any new library or pattern in one line. Small reversible edits over
  sweeping refactors. Solve only the current task.

## Honesty mechanics

- **Test what you control, mock what you don't.** The testing pattern: test
  prompt *formatting*, not API calls; mock at the API boundary; save real
  calls for manual eval runs. Fast tests that run every session beat
  integration tests that never run.
- **Findings over reassurance.** "4/4 (100%)" was written up as a failure of
  the eval set, not a success of the retriever. A metric that can't fail
  measures nothing — and the docs say so where the next reader will look.
- **Checkpoints state what is *verified* working**, against which corpus and
  config. Partial is labeled partial.

## Operational guardrails

- **Environment quirks get documented where they'll bite.** The embedded
  vector store allows one process at a time — so "stop Streamlit first" is in
  the project CLAUDE.md, the script's docstring, the state file, *and* the
  next-chat prompt. Redundancy is fine here: the constraint is invisible until
  it deadlocks you.
- **Known-good workflow block:** the exact commands (venv activation, index
  build, app launch, flags included) live in CLAUDE.md — no re-derivation,
  no drift.
- **Stale-state hygiene:** changing the corpus requires a fresh collection
  name; otherwise old vectors silently pollute results. Learned the hard way,
  then written down.
- **Cost ledger** (`docs/costs.md`): a running estimate of API spend with a
  price sheet, per-operation cost model, and per-session ledger appended at
  handoff. Even when totals are trivial (<1¢), the habit means the first
  genuinely expensive step (LLM-judge metrics) gets estimated *before* it
  runs, not invoiced after.
- **Commit identity checked, not assumed** — a personal project gets the
  personal email; verify `git config user.email` before committing, because
  history rewrites are worse than a ten-second check.

## The meta-guardrail

Every rule above earned its place by preventing a failure this project
actually experienced or came one step from experiencing. That's the
maintenance test for the harness itself: a guardrail that never fires and
maps to no plausible failure is instruction-budget noise — prune it.
