# Chip Huyen AI Engineering notes for this project

This file is a short working summary for our RAG build.

## What matters for this project
- Evaluation is central, not optional.
- Prompt engineering matters because instructions and context strongly affect outputs.
- RAG helps improve answer quality by supplying external context.
- Dataset quality matters, including document cleanliness and chunk quality.
- Good architecture includes retrieval, guardrails, evaluation, and feedback loops.

## How this applies to our app
- We must inspect source documents before indexing.
- Chunking strategy affects retrieval quality.
- Prompt design must tell the model to use retrieved context and ignore malicious instructions inside documents.
- We should return sources to the user.
- We should evaluate with a small test set instead of trusting subjective impressions.