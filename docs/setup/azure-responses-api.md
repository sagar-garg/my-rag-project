# Azure OpenAI Responses API setup notes

## We are using
- Azure OpenAI through Azure endpoint
- Responses API style integration
- A cheaper deployed model for runtime
- GPT-5.4 in Cursor for coding help, not app runtime

## Required environment variables

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_CHAT_DEPLOYMENT`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`

## Important principles
- Keep runtime model inexpensive
- Keep model configuration in environment variables
- Do not hardcode endpoints or keys
- Keep the first version stateless unless statefulness becomes necessary

## Deployment roles

- `AZURE_OPENAI_CHAT_DEPLOYMENT` is for answer generation.
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` is for indexing and retrieval.
- These are different jobs and usually different deployments.
- A chat deployment like `gpt-4o` should not be reused as the embedding deployment.

## API version requirement

- Azure OpenAI `responses.create()` requires `2025-03-01-preview` or later.
- Embedding calls can succeed on older API versions, which can be confusing during debugging.
- If embeddings work but answer generation fails with a `BadRequest` about Responses API support, the first thing to check is `AZURE_OPENAI_API_VERSION`.

## What the app must support
- simple request/response
- optional streaming
- retrieved context passed into generation
- citations in the final answer
- clear error handling

## Smoke-test setup that worked

- Chat deployment set separately from the embedding deployment
- Azure embedding model returning 1536-dimensional vectors
- `AZURE_OPENAI_API_VERSION=2025-03-01-preview`
- Local app run from `.venv`

## Troubleshooting

- If indexing fails before Qdrant is touched, verify the embedding deployment name first.
- If generation fails but indexing works, check the Azure API version before changing prompts or retrieval logic.
- If the app works in a one-off Python command but fails inside a long-running UI process, compare the runtime environment rather than assuming the code changed.