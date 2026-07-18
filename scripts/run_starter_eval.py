"""Baseline retrieval eval: do the starter questions reach the right chapter?

Retrieval-only — one embedding call per question, no chat API cost.
A question is a hit (hit@k) if any retrieved chunk comes from the expected
chapter PDF; the table also shows the first on-target rank and purity.

NOTE: the local embedded Qdrant store allows a single process at a time —
stop Streamlit before running this.

    .venv/bin/python -m scripts.run_starter_eval [--out PATH]
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from app.clients import build_qdrant_client
from app.config import PROJECT_ROOT, AppConfig
from app.eval.basic_eval import (
    RetrievalJudgment,
    judge_retrieval,
    load_starter_eval_cases,
)
from app.retrieval.search import search_chunks

STARTER_EVAL_PATH = PROJECT_ROOT / "data" / "eval" / "chapters_4_6_starter.json"
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT / "docs" / "showcase" / "eval" / f"{date.today().isoformat()}-baseline.md"
)


def _shorten(text: str, max_length: int = 48) -> str:
    return text if len(text) <= max_length else text[: max_length - 1] + "…"


def _chapter_label(file_name: str) -> str:
    """Compress `Chapter_6_RAG_and_Agents.pdf` to `Ch6` for compact tables."""

    parts = file_name.split("_")
    if len(parts) >= 2 and parts[0] == "Chapter":
        return f"Ch{parts[1]}"
    return file_name


def print_report(judgments: list[RetrievalJudgment], top_k: int) -> None:
    print(f"\nStarter eval — retrieval only, hit@{top_k}\n")
    header = f"{'Question':<50} {'Expected':<10} {'Result':<7} {'Rank':<5} On-target"
    print(header)
    print("-" * len(header))
    for judgment in judgments:
        expected = ", ".join(
            _chapter_label(name) for name in judgment.case.target_sources
        )
        result = "HIT" if judgment.hit else "MISS"
        rank = str(judgment.first_hit_rank) if judgment.first_hit_rank else "—"
        print(
            f"{_shorten(judgment.case.question):<50} {expected:<10} "
            f"{result:<7} {rank:<5} {judgment.on_target_count}/{len(judgment.retrieved_file_names)}"
        )

    hits = sum(1 for judgment in judgments if judgment.hit)
    print(f"\nHit rate: {hits}/{len(judgments)} ({hits / len(judgments):.0%})")


def render_markdown(
    judgments: list[RetrievalJudgment],
    config: AppConfig,
) -> str:
    hits = sum(1 for judgment in judgments if judgment.hit)
    total = len(judgments)

    lines = [
        f"# Baseline retrieval eval — {date.today().isoformat()}",
        "",
        f"**Hit rate: {hits}/{total} ({hits / total:.0%})** — hit@{config.top_k}, "
        "retrieval only (no generation).",
        "",
        "A question counts as a hit if any retrieved chunk comes from the expected "
        "chapter PDF. Rank is the position of the first on-target chunk (1 = best).",
        "",
        "## Configuration",
        "",
        f"- Collection: `{config.qdrant_collection_name}` (local embedded Qdrant)",
        f"- Chunking: size {config.chunk_size}, overlap {config.chunk_overlap}",
        f"- Retrieval: dense top-{config.top_k}",
        f"- Embeddings: `{config.embedding_deployment_name}`",
        "",
        "## Per-question results",
        "",
        "| # | Question | Expected | Result | First-hit rank | On-target | Retrieved (by rank) |",
        "|---|----------|----------|--------|----------------|-----------|---------------------|",
    ]
    for index, judgment in enumerate(judgments, start=1):
        expected = ", ".join(
            _chapter_label(name) for name in judgment.case.target_sources
        )
        result = "✅ hit" if judgment.hit else "❌ miss"
        rank = str(judgment.first_hit_rank) if judgment.first_hit_rank else "—"
        retrieved = ", ".join(
            _chapter_label(name) for name in judgment.retrieved_file_names
        )
        lines.append(
            f"| {index} | {judgment.case.question} | {expected} | {result} "
            f"| {rank} | {judgment.on_target_count}/{len(judgment.retrieved_file_names)} "
            f"| {retrieved} |"
        )

    lines += [
        "",
        "## Observations",
        "",
        "_TODO: notes on misses and near-misses — this feeds the case study._",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Markdown artifact path (default: docs/showcase/eval/<today>-baseline.md)",
    )
    args = parser.parse_args()

    config = AppConfig.from_env()
    qdrant_client = build_qdrant_client(config)
    if not qdrant_client.collection_exists(config.qdrant_collection_name):
        raise SystemExit(
            f"Collection `{config.qdrant_collection_name}` does not exist. "
            "Run `.venv/bin/python -m app.indexing.build_index` first."
        )

    cases = load_starter_eval_cases(STARTER_EVAL_PATH)
    judgments = []
    for case in cases:
        chunks = search_chunks(case.question, config=config, client=qdrant_client)
        judgments.append(
            judge_retrieval(case, [chunk.file_name for chunk in chunks])
        )

    print_report(judgments, config.top_k)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_markdown(judgments, config), encoding="utf-8")
    print(f"\nArtifact written: {args.out}")


if __name__ == "__main__":
    main()
