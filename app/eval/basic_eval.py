from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Sequence


@dataclass(frozen=True)
class EvalSample:
    question: str
    answer: str
    reference_answer: str
    retrieved_contexts: list[str]


@dataclass(frozen=True)
class StarterEvalCase:
    question: str
    reference_answer: str
    target_sources: list[str]


def load_starter_eval_cases(data_path: Path) -> list[StarterEvalCase]:
    """Load a tiny hand-written evaluation set from a JSON file."""

    raw_items = json.loads(data_path.read_text(encoding="utf-8"))
    if not isinstance(raw_items, list):
        raise ValueError("Starter evaluation data must be a JSON list.")

    cases: list[StarterEvalCase] = []
    for index, raw_item in enumerate(raw_items):
        if not isinstance(raw_item, dict):
            raise ValueError(
                f"Starter evaluation item {index} must be a JSON object."
            )

        question = raw_item.get("question")
        reference_answer = raw_item.get("reference_answer")
        target_sources = raw_item.get("target_sources")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(
                f"Starter evaluation item {index} must include a non-empty `question`."
            )
        if not isinstance(reference_answer, str) or not reference_answer.strip():
            raise ValueError(
                "Starter evaluation item "
                f"{index} must include a non-empty `reference_answer`."
            )
        if not isinstance(target_sources, list) or not target_sources:
            raise ValueError(
                "Starter evaluation item "
                f"{index} must include a non-empty `target_sources` list."
            )
        if not all(isinstance(source, str) and source.strip() for source in target_sources):
            raise ValueError(
                "Starter evaluation item "
                f"{index} must use non-empty string source names."
            )

        cases.append(
            StarterEvalCase(
                question=question.strip(),
                reference_answer=reference_answer.strip(),
                target_sources=[source.strip() for source in target_sources],
            )
        )

    if not cases:
        raise ValueError("At least one starter evaluation case is required.")
    return cases


def build_eval_sample(
    case: StarterEvalCase,
    *,
    answer: str,
    retrieved_contexts: list[str],
) -> EvalSample:
    """Fill a starter case with runtime answer and retrieval context."""

    return EvalSample(
        question=case.question,
        answer=answer,
        reference_answer=case.reference_answer,
        retrieved_contexts=retrieved_contexts,
    )


def build_ragas_dataset(samples: list[EvalSample]) -> Any:
    """Convert plain Python samples into a Ragas evaluation dataset."""

    if not samples:
        raise ValueError("At least one evaluation sample is required.")

    from ragas.dataset_schema import EvaluationDataset, SingleTurnSample

    ragas_samples = [
        SingleTurnSample(
            user_input=sample.question,
            response=sample.answer,
            reference=sample.reference_answer,
            retrieved_contexts=sample.retrieved_contexts,
        )
        for sample in samples
    ]
    return EvaluationDataset(samples=ragas_samples)


def run_ragas_evaluation(
    samples: list[EvalSample],
    *,
    metrics: Sequence[Any],
) -> Any:
    """Run a minimal Ragas evaluation with caller-provided metrics."""

    if not metrics:
        raise ValueError("Pass at least one Ragas metric to run evaluation.")

    from ragas import evaluate

    dataset = build_ragas_dataset(samples)
    return evaluate(dataset=dataset, metrics=list(metrics))
