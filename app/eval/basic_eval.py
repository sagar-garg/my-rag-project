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


@dataclass(frozen=True)
class RetrievalJudgment:
    case: StarterEvalCase
    retrieved_file_names: list[str]
    hit: bool
    first_hit_rank: int | None
    on_target_count: int


def judge_retrieval(
    case: StarterEvalCase,
    retrieved_file_names: list[str],
) -> RetrievalJudgment:
    """Judge whether retrieval reached the expected source (hit@k).

    A hit means at least one retrieved chunk comes from a file named in
    `case.target_sources`. Ranks are 1-based.
    """

    target_names = set(case.target_sources)
    on_target_ranks = [
        rank
        for rank, file_name in enumerate(retrieved_file_names, start=1)
        if file_name in target_names
    ]

    return RetrievalJudgment(
        case=case,
        retrieved_file_names=list(retrieved_file_names),
        hit=bool(on_target_ranks),
        first_hit_rank=on_target_ranks[0] if on_target_ranks else None,
        on_target_count=len(on_target_ranks),
    )


@dataclass(frozen=True)
class RetrievalSummary:
    """Aggregate retrieval metrics across an eval run.

    Rank aggregates cover only questions with at least one on-target chunk;
    they are None when every question missed.
    """

    question_count: int
    hit_count: int
    on_target_total: int
    retrieved_total: int
    mean_first_hit_rank: float | None
    worst_first_hit_rank: int | None


def summarize_judgments(judgments: list[RetrievalJudgment]) -> RetrievalSummary:
    """Aggregate per-question judgments into run-level metrics."""

    if not judgments:
        raise ValueError("At least one judgment is required.")

    first_hit_ranks = [
        judgment.first_hit_rank
        for judgment in judgments
        if judgment.first_hit_rank is not None
    ]
    return RetrievalSummary(
        question_count=len(judgments),
        hit_count=sum(1 for judgment in judgments if judgment.hit),
        on_target_total=sum(judgment.on_target_count for judgment in judgments),
        retrieved_total=sum(
            len(judgment.retrieved_file_names) for judgment in judgments
        ),
        mean_first_hit_rank=(
            sum(first_hit_ranks) / len(first_hit_ranks) if first_hit_ranks else None
        ),
        worst_first_hit_rank=max(first_hit_ranks) if first_hit_ranks else None,
    )


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
