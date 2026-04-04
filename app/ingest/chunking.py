from __future__ import annotations

from uuid import NAMESPACE_URL, uuid5

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode


def chunk_documents(
    documents: list[Document],
    *,
    chunk_size: int,
    chunk_overlap: int,
) -> list[TextNode]:
    """Split documents into deterministic text chunks."""

    if not documents:
        return []

    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.get_nodes_from_documents(documents)

    chunk_counts_by_source: dict[str, int] = {}
    for chunk in chunks:
        source_path = str(chunk.metadata.get("source_path", "unknown"))
        chunk_index = chunk_counts_by_source.get(source_path, 0)
        chunk_counts_by_source[source_path] = chunk_index + 1

        chunk.metadata["chunk_index"] = chunk_index
        chunk.id_ = _build_chunk_id(source_path, chunk_index, chunk.text)

    return chunks


def _build_chunk_id(source_path: str, chunk_index: int, text: str) -> str:
    stable_key = f"{source_path}:{chunk_index}:{text[:80]}"
    return str(uuid5(NAMESPACE_URL, stable_key))
