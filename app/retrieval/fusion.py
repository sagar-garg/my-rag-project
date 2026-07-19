"""Reciprocal rank fusion for combining rankings from multiple retrievers."""

from __future__ import annotations


def reciprocal_rank_fusion(
    rankings: list[list[str]],
    *,
    k: int = 60,
) -> list[tuple[str, float]]:
    """Fuse rankings of chunk ids into one list ordered by RRF score.

    Each item scores sum(1 / (k + rank)) over the rankings it appears in,
    with rank starting at 1. Rank-based fusion needs no score normalization
    between retrievers whose scores live on different scales (cosine
    similarity vs BM25). Ties break on id so the output is deterministic.
    """

    if k < 0:
        raise ValueError("k must be non-negative.")

    fused_scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item_id in enumerate(ranking, start=1):
            fused_scores[item_id] = fused_scores.get(item_id, 0.0) + 1.0 / (k + rank)

    return sorted(fused_scores.items(), key=lambda pair: (-pair[1], pair[0]))
