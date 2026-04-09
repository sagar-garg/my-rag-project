from __future__ import annotations

from dataclasses import dataclass

from qdrant_client import models

from app.clients import build_qdrant_client, embed_texts
from app.config import AppConfig
from app.ingest.chunking import chunk_documents
from app.ingest.loaders import load_source_documents


@dataclass(frozen=True)
class IndexBuildResult:
    document_count: int
    chunk_count: int
    collection_name: str


def build_index(config: AppConfig) -> IndexBuildResult:
    """Load raw documents, chunk them, embed them, and store them in Qdrant."""

    documents = load_source_documents(
        config.raw_data_dir,
        allowed_file_names=set(config.source_file_names),
    )
    if not documents:
        selected_files = ", ".join(config.source_file_names)
        raise ValueError(
            f"No supported files were found in `{config.raw_data_dir}`. "
            "Add .md, .txt, .pdf, or .docx files first. "
            f"Current source filter: {selected_files}."
        )

    chunks = chunk_documents(
        documents,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    texts = [chunk.text for chunk in chunks]
    embeddings = _embed_in_batches(texts, config=config)

    qdrant_client = build_qdrant_client(config)
    _ensure_collection_exists(
        qdrant_client=qdrant_client,
        collection_name=config.qdrant_collection_name,
        vector_size=len(embeddings[0]),
    )

    points = [
        models.PointStruct(
            id=chunk.id_,
            vector=embedding,
            payload={
                "text": chunk.text,
                "source_path": chunk.metadata.get("source_path", "unknown"),
                "file_name": chunk.metadata.get("file_name", "unknown"),
                "chunk_index": chunk.metadata.get("chunk_index", 0),
            },
        )
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]
    qdrant_client.upsert(
        collection_name=config.qdrant_collection_name,
        points=points,
    )

    return IndexBuildResult(
        document_count=len(documents),
        chunk_count=len(chunks),
        collection_name=config.qdrant_collection_name,
    )


def _embed_in_batches(texts: list[str], *, config: AppConfig) -> list[list[float]]:
    all_embeddings: list[list[float]] = []
    for start_index in range(0, len(texts), config.embedding_batch_size):
        batch = texts[start_index : start_index + config.embedding_batch_size]
        all_embeddings.extend(embed_texts(batch, config=config))
    return all_embeddings


def _ensure_collection_exists(
    *,
    qdrant_client: object,
    collection_name: str,
    vector_size: int,
) -> None:
    exists = False
    if hasattr(qdrant_client, "collection_exists"):
        exists = bool(qdrant_client.collection_exists(collection_name=collection_name))
    else:
        try:
            qdrant_client.get_collection(collection_name=collection_name)
            exists = True
        except Exception:
            exists = False

    if exists:
        return

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )


def main() -> None:
    config = AppConfig.from_env()
    result = build_index(config)
    print(
        "Indexed "
        f"{result.document_count} documents into `{result.collection_name}` "
        f"with {result.chunk_count} chunks."
    )


if __name__ == "__main__":
    main()
