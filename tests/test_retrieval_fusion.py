import pytest

from app.models import RetrievedChunk
from app.retrieval.fusion import reciprocal_rank_fusion
from app.retrieval.lexical import Bm25Index, tokenize


def _chunk(chunk_id: str, text: str, *, file_name: str = "doc.txt", chunk_index: int = 0) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=text,
        source_path=f"/data/{file_name}",
        file_name=file_name,
        chunk_index=chunk_index,
        score=0.0,
    )


# --- reciprocal_rank_fusion -------------------------------------------------


def test_rrf_agreement_across_rankings_beats_single_ranking_top_rank() -> None:
    rankings = [
        ["y", "x", "p"],
        ["q", "x", "r"],
    ]

    fused = dict(reciprocal_rank_fusion(rankings))

    assert fused["x"] > fused["y"]
    ids_in_order = [item_id for item_id, _ in reciprocal_rank_fusion(rankings)]
    assert ids_in_order[0] == "x"


def test_rrf_item_in_single_ranking_still_scored_and_present() -> None:
    rankings = [
        ["y", "x", "p"],
        ["q", "x", "r"],
    ]

    fused = dict(reciprocal_rank_fusion(rankings))

    assert "p" in fused
    assert fused["p"] == pytest.approx(1.0 / 63)


def test_rrf_exact_score_arithmetic_default_k() -> None:
    fused = dict(reciprocal_rank_fusion([["a"], ["a"]]))

    assert fused["a"] == pytest.approx(2.0 / 61)


def test_rrf_tie_break_is_deterministic_by_id() -> None:
    fused = reciprocal_rank_fusion([["b"], ["a"]])

    assert fused[0][1] == pytest.approx(fused[1][1])
    assert [item_id for item_id, _ in fused] == ["a", "b"]


def test_rrf_k_zero_is_allowed() -> None:
    fused = dict(reciprocal_rank_fusion([["a", "b"]], k=0))

    assert fused["a"] == pytest.approx(1.0)
    assert fused["b"] == pytest.approx(0.5)


def test_rrf_negative_k_raises() -> None:
    with pytest.raises(ValueError):
        reciprocal_rank_fusion([["a"]], k=-1)


def test_rrf_empty_rankings_returns_empty_list() -> None:
    assert reciprocal_rank_fusion([]) == []


# --- tokenize ----------------------------------------------------------------


def test_tokenize_lowercases_and_splits_on_non_alphanumerics() -> None:
    assert tokenize("RAG-based, agents!") == ["rag", "based", "agents"]


# --- Bm25Index -----------------------------------------------------------------


def _distinctive_corpus() -> list[RetrievedChunk]:
    return [
        _chunk("doc0", "the cat sat on the mat zebra", file_name="cats.txt"),
        _chunk("doc1", "the dog sat on the log", file_name="dogs.txt"),
        _chunk("doc2", "the bird flew over the tree", file_name="birds.txt"),
    ]


def test_bm25_distinctive_term_ranks_matching_doc_first() -> None:
    index = Bm25Index(_distinctive_corpus())

    results = index.search("the zebra", top_k=3)

    assert results[0].chunk_id == "doc0"


def test_bm25_ubiquitous_term_scores_near_zero_relative_to_rare_term() -> None:
    index = Bm25Index(_distinctive_corpus())

    ubiquitous_scores = index.score("the")
    rare_scores = index.score("zebra")

    assert max(rare_scores) > 3 * max(ubiquitous_scores)


def test_bm25_length_normalization_favors_shorter_doc() -> None:
    chunks = [
        _chunk("short", "keyword"),
        _chunk("long", "keyword filler filler filler filler filler filler filler filler filler"),
    ]
    index = Bm25Index(chunks)

    scores = index.score("keyword")

    short_index = [chunk.chunk_id for chunk in chunks].index("short")
    long_index = [chunk.chunk_id for chunk in chunks].index("long")
    assert scores[short_index] > scores[long_index]


def test_bm25_search_excludes_zero_score_docs() -> None:
    index = Bm25Index(_distinctive_corpus())

    results = index.search("zebra", top_k=10)

    assert len(results) == 1
    assert results[0].chunk_id == "doc0"


def test_bm25_search_results_carry_score_and_metadata() -> None:
    index = Bm25Index(_distinctive_corpus())

    results = index.search("zebra", top_k=1)

    assert len(results) == 1
    result = results[0]
    assert result.score > 0
    assert result.file_name == "cats.txt"
    assert result.source_path == "/data/cats.txt"
    assert result.chunk_index == 0


def test_bm25_index_rejects_empty_corpus() -> None:
    with pytest.raises(ValueError):
        Bm25Index([])
