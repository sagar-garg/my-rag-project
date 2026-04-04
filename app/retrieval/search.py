from __future__ import annotations

from app.clients import build_qdrant_client, embed_texts
from app.config import AppConfig
from app.models import RetrievedChunk


def search_chunks(
    question: str,
    *,
    config: AppConfig,
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Retrieve the top-k most similar chunks from Qdrant."""

    clean_question = question.strip()
    if not clean_question:
        raise ValueError("Question cannot be empty.")

    query_embedding = embed_texts([clean_question], config=config)[0]
    qdrant_client = build_qdrant_client(config)
    search_limit = top_k or config.top_k

    search_result = qdrant_client.query_points(
        collection_name=config.qdrant_collection_name,
        query=query_embedding,
        limit=search_limit,
        with_payload=True,
    )

    return [
        RetrievedChunk(
            chunk_id=str(point.id),
            text=str(point.payload.get("text", "")),
            source_path=str(point.payload.get("source_path", "unknown")),
            file_name=str(point.payload.get("file_name", "unknown")),
            chunk_index=int(point.payload.get("chunk_index", 0)),
            score=float(point.score or 0.0),
        )
        for point in search_result.points
    ]
