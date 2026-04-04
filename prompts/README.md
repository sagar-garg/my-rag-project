# Prompts Workflow

This folder is for chat workflow, not for durable project documentation.

## Structure

- `archive/`: frozen historical prompt sets
- `current/project-state.md`: short snapshot of what the project is today
- `current/next-chat.md`: the best next prompt to use in the next conversation
- `current/backlog.md`: future tasks that are not yet the next priority
- `templates/`: reusable prompt shapes for feature work, debugging, and end-of-chat handoff

## Rule of thumb

- If it is still true about the project next week, put it in `docs/`.
- If it is mainly about what to do in the next chat, put it in `prompts/current/`.
- If it describes how we used to think about the project, archive it.
