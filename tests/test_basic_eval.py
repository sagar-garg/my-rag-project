from pathlib import Path

from app.eval.basic_eval import build_eval_sample, load_starter_eval_cases


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STARTER_EVAL_PATH = PROJECT_ROOT / "data" / "eval" / "chapters_4_6_starter.json"


def test_load_starter_eval_cases_reads_expected_chapter_sources() -> None:
    cases = load_starter_eval_cases(STARTER_EVAL_PATH)

    assert len(cases) == 4
    assert cases[0].target_sources == ["Chapter_4_Evaluate_AI_Systems.pdf"]
    assert cases[1].target_sources == ["Chapter_5_Prompt_Engineering.pdf"]
    assert cases[2].target_sources == ["Chapter_6_RAG_and_Agents.pdf"]


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
