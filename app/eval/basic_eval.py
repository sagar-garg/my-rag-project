from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class EvalSample:
    question: str
    answer: str
    reference_answer: str
    retrieved_contexts: list[str]


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
