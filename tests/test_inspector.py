from app.eval.basic_eval import StarterEvalCase
from app.ui.inspector import chapter_label, find_matching_case, score_caption

import pytest


def _case(question: str) -> StarterEvalCase:
    return StarterEvalCase(
        question=question,
        reference_answer="unused",
        target_sources=["Chapter_5_Prompt_Engineering.pdf"],
    )


# --- chapter_label ---


def test_chapter_label_compresses_chapter_file_names():
    assert chapter_label("Chapter_6_RAG_and_Agents.pdf") == "Ch6"


def test_chapter_label_passes_through_non_chapter_names():
    assert chapter_label("notes.md") == "notes.md"


# --- find_matching_case ---


def test_find_matching_case_exact_match():
    cases = [_case("Where should important information go?")]
    assert find_matching_case("Where should important information go?", cases) is cases[0]


def test_find_matching_case_normalizes_whitespace_and_case():
    cases = [_case("Where should important information go?")]
    typed = "  where should  IMPORTANT information go?\n"
    assert find_matching_case(typed, cases) is cases[0]


def test_find_matching_case_returns_none_without_match():
    cases = [_case("Where should important information go?")]
    assert find_matching_case("Something else entirely", cases) is None


def test_find_matching_case_empty_question_matches_nothing():
    assert find_matching_case("   ", [_case("A question?")]) is None


# --- score_caption ---


def test_score_caption_covers_all_modes():
    for mode in ("dense", "hybrid", "rerank"):
        assert score_caption(mode)


def test_score_caption_rejects_unknown_mode():
    with pytest.raises(ValueError):
        score_caption("bm25")
