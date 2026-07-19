from __future__ import annotations

from qdrant_client import QdrantClient

from app.clients import build_qdrant_client, embed_texts
from app.config import AppConfig
from app.models import RetrievedChunk
from app.retrieval.fusion import reciprocal_rank_fusion
from app.retrieval.lexical import Bm25Index

CANDIDATE_MULTIPLIER = 3


def search_chunks(
    question: str,
    *,
    config: AppConfig,
    top_k: int | None = None,
    client: QdrantClient | None = None,
) -> list[RetrievedChunk]:
    """Retrieve the top-k most similar chunks from Qdrant.

    Pass `client` to reuse one connection across calls — required with the
    local embedded store, which allows only one client instance at a time.
    """

    clean_question = question.strip()
    if not clean_question:
        raise ValueError("Question cannot be empty.")

    query_embedding = embed_texts([clean_question], config=config)[0]
    qdrant_client = client or build_qdrant_client(config)
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


def search_chunks_hybrid(
    question: str,
    *,
    config: AppConfig,
    bm25_index: Bm25Index,
    top_k: int | None = None,
    client: QdrantClient | None = None,
) -> list[RetrievedChunk]:
    """Hybrid retrieval: dense + BM25 candidates fused with reciprocal rank
    fusion, top-k of the fused ranking returned.

    Each side contributes `top_k * CANDIDATE_MULTIPLIER` candidates so the
    lexical ranking can promote chunks that dense retrieval ranked below
    top-k. The returned `score` is the RRF score, not cosine similarity.
    """

    final_k = top_k or config.top_k
    candidate_k = final_k * CANDIDATE_MULTIPLIER

    dense_candidates = search_chunks(
        question, config=config, top_k=candidate_k, client=client
    )
    lexical_candidates = bm25_index.search(question, top_k=candidate_k)

    chunks_by_id = {chunk.chunk_id: chunk for chunk in dense_candidates}
    chunks_by_id.update(
        {chunk.chunk_id: chunk for chunk in lexical_candidates}
    )

    fused = reciprocal_rank_fusion(
        [
            [chunk.chunk_id for chunk in dense_candidates],
            [chunk.chunk_id for chunk in lexical_candidates],
        ]
    )

    return [
        RetrievedChunk(
            chunk_id=chunk_id,
            text=chunks_by_id[chunk_id].text,
            source_path=chunks_by_id[chunk_id].source_path,
            file_name=chunks_by_id[chunk_id].file_name,
            chunk_index=chunks_by_id[chunk_id].chunk_index,
            score=rrf_score,
        )
        for chunk_id, rrf_score in fused[:final_k]
    ]
