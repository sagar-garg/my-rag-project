from pathlib import Path

import pytest

from app.eval.basic_eval import (
    StarterEvalCase,
    build_eval_sample,
    judge_retrieval,
    load_starter_eval_cases,
    summarize_judgments,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STARTER_EVAL_PATH = PROJECT_ROOT / "data" / "eval" / "chapters_4_6_starter.json"


def test_load_starter_eval_cases_reads_expected_chapter_sources() -> None:
    cases = load_starter_eval_cases(STARTER_EVAL_PATH)

    assert len(cases) == 15
    assert cases[0].target_sources == ["Chapter_4_Evaluate_AI_Systems.pdf"]
    assert cases[1].target_sources == ["Chapter_5_Prompt_Engineering.pdf"]
    assert cases[2].target_sources == ["Chapter_6_RAG_and_Agents.pdf"]
    assert cases[13].target_sources == [
        "Chapter_5_Prompt_Engineering.pdf",
        "Chapter_6_RAG_and_Agents.pdf",
    ]


def test_build_eval_sample_copies_reference_fields() -> None:
    case = load_starter_eval_cases(STARTER_EVAL_PATH)[0]

    sample = build_eval_sample(
        case,
        answer="Evaluation-driven development means deciding how to measure success before building.",
        retrieved_contexts=["Evaluation-driven development means defining evaluation criteria before building."],
    )

    assert sample.question == case.question
    assert sample.reference_answer == case.reference_answer
    assert sample.answer.startswith("Evaluation-driven development")
    assert len(sample.retrieved_contexts) == 1


def _case(target_sources: list[str]) -> StarterEvalCase:
    return StarterEvalCase(
        question="What is X?",
        reference_answer="X is Y.",
        target_sources=target_sources,
    )


def test_judge_retrieval_hit_at_rank_one() -> None:
    judgment = judge_retrieval(
        _case(["Chapter_4_Evaluate_AI_Systems.pdf"]),
        [
            "Chapter_4_Evaluate_AI_Systems.pdf",
            "Chapter_5_Prompt_Engineering.pdf",
            "Chapter_4_Evaluate_AI_Systems.pdf",
            "Chapter_6_RAG_and_Agents.pdf",
        ],
    )

    assert judgment.hit is True
    assert judgment.first_hit_rank == 1
    assert judgment.on_target_count == 2


def test_judge_retrieval_hit_at_lower_rank() -> None:
    judgment = judge_retrieval(
        _case(["Chapter_6_RAG_and_Agents.pdf"]),
        [
            "Chapter_5_Prompt_Engineering.pdf",
            "Chapter_5_Prompt_Engineering.pdf",
            "Chapter_6_RAG_and_Agents.pdf",
            "Chapter_4_Evaluate_AI_Systems.pdf",
        ],
    )

    assert judgment.hit is True
    assert judgment.first_hit_rank == 3
    assert judgment.on_target_count == 1


def test_judge_retrieval_miss() -> None:
    judgment = judge_retrieval(
        _case(["Chapter_6_RAG_and_Agents.pdf"]),
        [
            "Chapter_4_Evaluate_AI_Systems.pdf",
            "Chapter_5_Prompt_Engineering.pdf",
        ],
    )

    assert judgment.hit is False
    assert judgment.first_hit_rank is None
    assert judgment.on_target_count == 0


def test_summarize_judgments_aggregates_purity_and_ranks() -> None:
    ch4 = "Chapter_4_Evaluate_AI_Systems.pdf"
    ch5 = "Chapter_5_Prompt_Engineering.pdf"
    judgments = [
        judge_retrieval(_case([ch4]), [ch4, ch4, ch5, ch4]),
        judge_retrieval(_case([ch5]), [ch4, ch5, ch5, ch4]),
        judge_retrieval(_case([ch5]), [ch4, ch4, ch4, ch4]),
    ]

    summary = summarize_judgments(judgments)

    assert summary.question_count == 3
    assert summary.hit_count == 2
    assert summary.on_target_total == 5
    assert summary.retrieved_total == 12
    assert summary.mean_first_hit_rank == pytest.approx(1.5)
    assert summary.worst_first_hit_rank == 2


def test_summarize_judgments_all_misses_has_no_ranks() -> None:
    ch4 = "Chapter_4_Evaluate_AI_Systems.pdf"
    ch5 = "Chapter_5_Prompt_Engineering.pdf"
    judgments = [judge_retrieval(_case([ch5]), [ch4, ch4])]

    summary = summarize_judgments(judgments)

    assert summary.hit_count == 0
    assert summary.mean_first_hit_rank is None
    assert summary.worst_first_hit_rank is None


def test_summarize_judgments_rejects_empty_list() -> None:
    with pytest.raises(ValueError):
        summarize_judgments([])


def test_judge_retrieval_multiple_target_sources() -> None:
    judgment = judge_retrieval(
        _case(
            [
                "Chapter_5_Prompt_Engineering.pdf",
                "Chapter_6_RAG_and_Agents.pdf",
            ]
        ),
        [
            "Chapter_4_Evaluate_AI_Systems.pdf",
            "Chapter_6_RAG_and_Agents.pdf",
        ],
    )

    assert judgment.hit is True
    assert judgment.first_hit_rank == 2
    assert judgment.on_target_count == 1
