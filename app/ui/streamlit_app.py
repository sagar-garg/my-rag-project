from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st
from qdrant_client import QdrantClient

# Streamlit runs file paths directly, so we add the repo root
# to sys.path before importing from the `app` package.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.clients import build_azure_openai_client, build_qdrant_client
from app.config import AppConfig
from app.eval.basic_eval import (
    StarterEvalCase,
    judge_retrieval,
    load_starter_eval_cases,
)
from app.generation.respond import generate_answer
from app.indexing.build_index import build_index
from app.models import RetrievedChunk
from app.retrieval.lexical import Bm25Index, load_corpus
from app.retrieval.rerank import search_chunks_reranked
from app.retrieval.search import search_chunks, search_chunks_hybrid
from app.ui.inspector import chapter_label, find_matching_case, score_caption

EVAL_SET_PATH = PROJECT_ROOT / "data" / "eval" / "chapters_4_6_starter.json"

MODE_LABELS = {
    "dense": "Dense (default)",
    "hybrid": "Hybrid (dense + BM25)",
    "rerank": "LLM rerank",
}


st.set_page_config(page_title="Learning-First RAG", page_icon="📚", layout="wide")


@st.cache_resource
def get_qdrant_client() -> QdrantClient:
    """One embedded-store client for the whole server process. The local
    store's flock allows a single client instance, and Streamlit reruns can
    briefly overlap — per-rerun clients race for the lock."""

    return build_qdrant_client(AppConfig.from_env())


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

    mode = render_sidebar(config)
    render_question_flow(config, mode)


def render_sidebar(config: AppConfig) -> str:
    st.sidebar.header("Retrieval mode")
    mode = st.sidebar.radio(
        "Retrieval mode",
        options=list(MODE_LABELS),
        format_func=MODE_LABELS.get,
        label_visibility="collapsed",
        help=(
            "All three modes were measured against the 15-question eval set; "
            "dense won on purity. See docs/showcase/eval/."
        ),
    )
    if mode == "rerank":
        st.sidebar.caption(
            f"One extra LLM call per query on `{config.judge_deployment_name}` "
            "(~\\$0.003/query on a mini-tier judge; ~\\$0.014 on full gpt-4o)."
        )

    st.sidebar.header("Indexing")
    st.sidebar.write(
        "1. Put `.md`, `.txt`, `.pdf`, or `.docx` files in `data/raw/`.\n"
        "2. Click the button below to embed and store them in Qdrant."
    )

    if st.sidebar.button("Build or Refresh Index", use_container_width=True):
        # build_index opens its own client, so release the shared one first.
        get_qdrant_client().close()
        get_qdrant_client.clear()
        with st.spinner("Loading, chunking, embedding, and indexing documents..."):
            result = build_index(config)
        for key in [k for k in st.session_state if k.startswith("bm25_")]:
            del st.session_state[key]
        st.sidebar.success(
            "Indexed "
            f"{result.document_count} documents into `{result.collection_name}` "
            f"with {result.chunk_count} chunks."
        )

    return mode


def retrieve_chunks(
    question: str, *, mode: str, config: AppConfig, top_k: int
) -> tuple[list[RetrievedChunk], tuple[int, int] | None]:
    """Run retrieval in the selected mode. Returns (chunks, rerank token usage)."""

    client = get_qdrant_client()
    if mode == "rerank":
        result = search_chunks_reranked(
            question,
            config=config,
            client=client,
            azure_client=build_azure_openai_client(config),
            top_k=top_k,
        )
        return result.chunks, (result.input_tokens, result.output_tokens)
    if mode == "hybrid":
        cache_key = f"bm25_{config.qdrant_collection_name}"
        if cache_key not in st.session_state:
            st.session_state[cache_key] = Bm25Index(
                load_corpus(client, config.qdrant_collection_name)
            )
        chunks = search_chunks_hybrid(
            question,
            config=config,
            bm25_index=st.session_state[cache_key],
            top_k=top_k,
            client=client,
        )
        return chunks, None
    return search_chunks(question, config=config, top_k=top_k, client=client), None


def render_question_flow(config: AppConfig, mode: str) -> None:
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

        with st.spinner(f"Retrieving ({MODE_LABELS[mode]}) and generating an answer..."):
            chunks, rerank_usage = retrieve_chunks(
                question, mode=mode, config=config, top_k=top_k
            )
            answer = generate_answer(question, chunks=chunks, config=config)

        st.subheader("Answer")
        st.write(answer.answer_text)

        render_inspector(question, answer.cited_chunks, mode, config, rerank_usage)


def _load_eval_cases() -> list[StarterEvalCase]:
    if not EVAL_SET_PATH.exists():
        return []
    return load_starter_eval_cases(EVAL_SET_PATH)


def render_inspector(
    question: str,
    chunks: list[RetrievedChunk],
    mode: str,
    config: AppConfig,
    rerank_usage: tuple[int, int] | None,
) -> None:
    st.subheader("Retrieval inspector")
    st.caption(score_caption(mode))
    if rerank_usage is not None:
        input_tokens, output_tokens = rerank_usage
        st.caption(
            f"Rerank call: {input_tokens} input + {output_tokens} output tokens "
            f"on `{config.judge_deployment_name}`."
        )

    if not chunks:
        st.info("No chunks were retrieved.")
        return

    matched = find_matching_case(question, _load_eval_cases())
    targets: set[str] = set(matched.target_sources) if matched else set()
    if matched:
        judgment = judge_retrieval(matched, [chunk.file_name for chunk in chunks])
        expected = ", ".join(chapter_label(name) for name in matched.target_sources)
        purity = f"{judgment.on_target_count}/{len(judgment.retrieved_file_names)}"
        verdict = (
            f"Eval question — expected **{expected}** · "
            f"{'✅ hit' if judgment.hit else '❌ miss'} at rank "
            f"**{judgment.first_hit_rank or '—'}** · purity **{purity}**"
        )
        if judgment.hit and judgment.on_target_count == len(chunks):
            st.success(verdict)
        else:
            st.warning(verdict)

    for rank, chunk in enumerate(chunks, start=1):
        marker = ""
        if matched:
            marker = " ✅" if chunk.file_name in targets else " ❌"
        label = (
            f"[{rank}]{marker} {chapter_label(chunk.file_name)} · "
            f"chunk {chunk.chunk_index} · score {chunk.score:.3f}"
        )
        with st.expander(label, expanded=rank == 1):
            st.caption(chunk.source_path)
            st.write(chunk.text)


if __name__ == "__main__":
    main()
