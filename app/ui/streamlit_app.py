from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

# Streamlit runs file paths directly, so we add the repo root
# to sys.path before importing from the `app` package.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import AppConfig
from app.generation.respond import generate_answer
from app.indexing.build_index import build_index
from app.retrieval.search import search_chunks


st.set_page_config(page_title="Learning-First RAG", page_icon="📚")


def main() -> None:
    st.title("Learning-First RAG")
    st.caption(
        "A minimal Python RAG app using Azure OpenAI, LlamaIndex, Qdrant, and Streamlit."
    )

    try:
        config = AppConfig.from_env()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    render_sidebar(config)
    render_question_flow(config)


def render_sidebar(config: AppConfig) -> None:
    st.sidebar.header("Indexing")
    st.sidebar.write(
        "1. Put `.md`, `.txt`, `.pdf`, or `.docx` files in `data/raw/`.\n"
        "2. Click the button below to embed and store them in Qdrant."
    )

    if st.sidebar.button("Build or Refresh Index", use_container_width=True):
        with st.spinner("Loading, chunking, embedding, and indexing documents..."):
            result = build_index(config)
        st.sidebar.success(
            "Indexed "
            f"{result.document_count} documents into `{result.collection_name}` "
            f"with {result.chunk_count} chunks."
        )


def render_question_flow(config: AppConfig) -> None:
    st.subheader("Ask a question")
    question = st.text_area(
        "Question",
        placeholder="What do these documents say about chunking strategy?",
        height=100,
    )
    top_k = st.slider("Retrieved chunks", min_value=1, max_value=8, value=config.top_k)

    if st.button("Ask", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Enter a question before asking the app.")
            return

        with st.spinner("Retrieving context and generating an answer..."):
            chunks = search_chunks(question, config=config, top_k=top_k)
            answer = generate_answer(question, chunks=chunks, config=config)

        st.subheader("Answer")
        st.write(answer.answer_text)

        st.subheader("Sources")
        if not answer.cited_chunks:
            st.info("No sources were returned.")
            return

        for index, chunk in enumerate(answer.cited_chunks, start=1):
            with st.expander(
                f"[{index}] {chunk.source_path} | score={chunk.score:.3f}",
                expanded=index == 1,
            ):
                st.write(chunk.text)


if __name__ == "__main__":
    main()
