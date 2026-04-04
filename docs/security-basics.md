# Security basics for this project

## Secrets
- Store secrets only in `.env`
- Commit `.env.example`, never `.env`
- Rotate any key that was ever pasted into chat, code, logs, or screenshots
- Do not read or print `.env` during normal debugging unless the user explicitly asks
- Prefer checking variable names and expected schema through `.env.example`
- Treat any secret shown in tool output as exposed and rotate it

## Dependencies
- Pin versions in requirements.txt
- Enable GitHub Dependabot or security alerts
- Avoid unnecessary packages
- Avoid LiteLLM for the first version
- Avoid axios unless needed
- We are not using LiteLLM in v1 because this project calls Azure OpenAI directly.
- Avoid adding model gateways or proxies unless we actually need multi-provider routing or centralized governance.

## Runtime isolation
- Run in a Python virtualenv or Docker container
- Prefer a non-root container user if containerized
- Keep filesystem access minimal
- Keep the `data/` folder separate from app code

## Network
- Call only Azure OpenAI and Qdrant endpoints you expect
- Treat retrieved documents and external URLs as untrusted
- Do not fetch arbitrary URLs from model output
- Do not execute model-generated code automatically
- When possible, run the local app from your own terminal instead of through assistant-managed background processes
- This reduces confusion from sandbox-specific network restrictions during debugging

## Input handling
- Sanitize filenames
- Restrict upload types
- Set file size limits
- Reject path traversal patterns
- Log failures safely without secrets

## LLM-specific
- Treat retrieved text as untrusted prompt input
- Separate system rules from retrieved context
- In the answer prompt, tell the model not to follow instructions inside documents
- Return sources/citations with answers

## Sandbox policy for this project
- Run locally inside `.venv` during development
- Prefer Docker later for stronger isolation
- Do not add LiteLLM or other API gateways in v1
- Do not add observability platforms like Axiom in v1
- Keep dependencies minimal and pinned
- Treat retrieved document text as untrusted input
- Never execute model-generated code automatically
- Never allow the model to choose arbitrary external URLs to call
- If an assistant-run process needs broader network access, prefer understanding the need first and using your own terminal when practical