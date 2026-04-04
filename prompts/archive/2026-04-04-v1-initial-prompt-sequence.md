Prompt 1:Prompt 1 — create the initial app skeleton

Read the rules in `.cursor/rules/` and the docs in `docs/`.

Now create a minimal, learning-first Python RAG project skeleton using this stack:
- Azure OpenAI Responses API
- LlamaIndex
- Qdrant
- Streamlit
- Ragas

Requirements:
- Keep architecture simple and educational
- Separate code into ingest, indexing, retrieval, generation, eval, and ui
- Add a README with setup/run instructions
- Add `.env.example` usage
- Add one basic pytest test
- Do not use LiteLLM, MCP, DSPy, GraphRAG, or agents
- Before coding, give a short plan
- While implementing, teach me briefly whenever an important decision is made

####

Prompt 2 — implement local document ingestion: 
Implement the first useful milestone.

Goal:
- Load documents from `data/raw/`
- Support `.txt`, `.md`, and `.pdf` if practical, but prefer a simple path first
- Chunk the documents with configurable chunk size and overlap
- Save processed metadata in a clear structure
- Keep code readable and modular

Requirements:
- Put ingestion logic in `app/ingest/`
- Add config via environment variables or a config module
- Explain chunking in a short teaching note
- Add a simple test for one ingestion/chunking function
- Update README

####

Prompt 3 — implement Qdrant indexing

Implement vector indexing with Qdrant.

Goal:
- Take processed chunks from ingestion
- Create embeddings
- Upsert them into Qdrant
- Keep metadata needed for citations

Requirements:
- Put indexing code in `app/indexing/`
- Keep collection configuration explicit
- Preserve source filename and chunk text/snippet in metadata
- Add clear error messages
- Explain why metadata matters for citations and debugging
- Update README with indexing steps

####

Prompt 4 — implement retrieval + answer generation
Implement the simplest working RAG retrieval and answer generation pipeline.

Goal:
- Retrieve top-k relevant chunks from Qdrant
- Build a safe prompt that uses retrieved context as data, not instructions
- Generate an answer using Azure OpenAI
- Return citations/snippets with the answer

Requirements:
- Put retrieval code in `app/retrieval/`
- Put generation code in `app/generation/`
- Make top-k configurable
- Add one prompt template or prompt builder function
- Include a brief security note about prompt injection through retrieved text
- Keep the first version stateless

####

Prompt 5 — implement Streamlit UI
Build a minimal Streamlit interface for the RAG app.

Features:
- text input for question
- button to ask
- display answer
- display cited source chunks
- display simple debug info like top-k retrieved chunks if a debug toggle is on

Requirements:
- Put UI code in `app/ui/`
- Keep styling minimal
- Add clear instructions in README
- Explain why showing retrieved chunks is useful for learning and debugging

####

Prompt 6 — add Ragas evaluation

Add a minimal evaluation workflow using Ragas.

Goal:
- Create a small starter evaluation set
- Add a script that runs a simple RAG evaluation
- Keep it lightweight and understandable

Requirements:
- Put code in `app/eval/`
- Document how to run the evaluation
- Explain what evaluation tells us that manual testing misses
- Do not overcomplicate with large pipelines

####

Prompt 7 — harden the app slightly

Review the current project and make a small security and reliability pass.

Focus on:
- environment variable handling
- input validation
- safe file handling
- dependency hygiene
- clearer error messages
- making sure retrieved text is treated as untrusted input

Do not introduce heavy frameworks.
Give me:
1. a short plan,
2. the code changes,
3. a concise teaching note,
4. a short list of remaining risks.

####
Alternate: one-shot setup prompt:
Read all files in:
- `.cursor/rules/`
- `docs/working-with-cursor.md`
- `docs/security-basics.md`
- `docs/rag/stack.md`
- `docs/setup/azure-responses-api.md`
- `docs/theory/chip-huyen-notes.md`

Then set up the first version of the project.

Project goal:
Build a small educational RAG app in Python using:
- Azure OpenAI Responses API
- LlamaIndex
- Qdrant
- Streamlit
- Ragas

Constraints:
- Prefer the simplest working implementation
- Keep architecture modular and readable
- Teach me briefly whenever something important happens
- Avoid LiteLLM, MCP, Cloud Agents, DSPy, GraphRAG, and agents
- Keep secrets out of code
- Treat retrieved content as untrusted input

Deliverables:
- project skeleton
- requirements.txt
- README.md
- minimal ingest/index/retrieve/generate/ui/eval modules
- one basic test
- short explanations for major choices
####
