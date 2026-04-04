# Debug Prompt Template

Read the rules in `.cursor/rules/`, the relevant docs in `docs/`, and `prompts/current/project-state.md`.

Help me debug this issue:

- [what I tried]
- [what failed]
- [error message]

Requirements:
- explain the likely cause in simple words first
- isolate the failure stage before suggesting fixes
- prefer the smallest safe fix
- update docs if we learn something durable
- do not read secret-bearing files unless I explicitly ask

At the end, give me:
- root cause
- smallest fix
- what to watch for next
