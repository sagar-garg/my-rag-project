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

from app.clients import build_azure_openai_client, build_qdrant_client
from app.config import PROJECT_ROOT, AppConfig
from app.eval.basic_eval import (
    RetrievalJudgment,
    judge_retrieval,
    load_starter_eval_cases,
    summarize_judgments,
)
from app.retrieval.lexical import Bm25Index, load_corpus
from app.retrieval.rerank import search_chunks_reranked
from app.retrieval.search import (
    CANDIDATE_MULTIPLIER,
    search_chunks,
    search_chunks_hybrid,
)

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

    summary = summarize_judgments(judgments)
    print(f"\nHit rate: {summary.hit_count}/{summary.question_count} "
          f"({summary.hit_count / summary.question_count:.0%})")
    print(f"Purity: {summary.on_target_total}/{summary.retrieved_total} "
          f"({summary.on_target_total / summary.retrieved_total:.0%})")
    print(f"First-hit rank: mean {_format_rank(summary.mean_first_hit_rank)}, "
          f"worst {_format_rank(summary.worst_first_hit_rank)}")


def _format_rank(rank: float | int | None) -> str:
    if rank is None:
        return "—"
    return f"{rank:.2f}" if isinstance(rank, float) else str(rank)


def _retrieval_description(mode: str, config: AppConfig) -> str:
    if mode == "hybrid":
        return (
            f"hybrid (dense + BM25, RRF k=60, "
            f"{config.top_k * CANDIDATE_MULTIPLIER} candidates/side) top-{config.top_k}"
        )
    if mode == "rerank":
        return (
            f"LLM rerank ({config.judge_deployment_name}) of dense "
            f"top-{config.top_k * CANDIDATE_MULTIPLIER} → top-{config.top_k}"
        )
    return f"dense top-{config.top_k}"


def render_markdown(
    judgments: list[RetrievalJudgment],
    config: AppConfig,
    *,
    title: str = "Retrieval eval",
    mode: str = "dense",
) -> str:
    summary = summarize_judgments(judgments)
    hits = summary.hit_count
    total = summary.question_count

    lines = [
        f"# {title} — {date.today().isoformat()}",
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
        f"- Retrieval: {_retrieval_description(mode, config)}",
        f"- Embeddings: `{config.embedding_deployment_name}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Hit@{config.top_k} | {hits}/{total} ({hits / total:.0%}) |",
        f"| Purity (on-target chunks) | {summary.on_target_total}/{summary.retrieved_total} "
        f"({summary.on_target_total / summary.retrieved_total:.0%}) |",
        f"| Mean first-hit rank | {_format_rank(summary.mean_first_hit_rank)} |",
        f"| Worst first-hit rank | {_format_rank(summary.worst_first_hit_rank)} |",
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
    parser.add_argument(
        "--title",
        default="Retrieval eval",
        help='Artifact H1 title (default: "Retrieval eval")',
    )
    parser.add_argument(
        "--mode",
        choices=["dense", "hybrid", "rerank"],
        default="dense",
        help=(
            "Retrieval path: dense (default), hybrid (dense + BM25 via RRF), "
            "or rerank (LLM listwise rerank of dense candidates)"
        ),
    )
    args = parser.parse_args()

    config = AppConfig.from_env()
    qdrant_client = build_qdrant_client(config)
    if not qdrant_client.collection_exists(config.qdrant_collection_name):
        raise SystemExit(
            f"Collection `{config.qdrant_collection_name}` does not exist. "
            "Run `.venv/bin/python -m app.indexing.build_index` first."
        )

    bm25_index = None
    if args.mode == "hybrid":
        corpus = load_corpus(qdrant_client, config.qdrant_collection_name)
        bm25_index = Bm25Index(corpus)
        print(f"BM25 index built over {len(corpus)} chunks (local, no API).")

    azure_client = None
    if args.mode == "rerank":
        azure_client = build_azure_openai_client(config)

    cases = load_starter_eval_cases(STARTER_EVAL_PATH)
    judgments = []
    total_input_tokens = 0
    total_output_tokens = 0
    for case in cases:
        if args.mode == "rerank":
            rerank_result = search_chunks_reranked(
                case.question,
                config=config,
                client=qdrant_client,
                azure_client=azure_client,
            )
            chunks = rerank_result.chunks
            total_input_tokens += rerank_result.input_tokens
            total_output_tokens += rerank_result.output_tokens
        elif bm25_index is not None:
            chunks = search_chunks_hybrid(
                case.question,
                config=config,
                bm25_index=bm25_index,
                client=qdrant_client,
            )
        else:
            chunks = search_chunks(case.question, config=config, client=qdrant_client)
        judgments.append(
            judge_retrieval(case, [chunk.file_name for chunk in chunks])
        )

    print_report(judgments, config.top_k)

    if args.mode == "rerank":
        print(
            f"\nRerank chat usage: {total_input_tokens} input + "
            f"{total_output_tokens} output tokens across {len(cases)} calls"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        render_markdown(judgments, config, title=args.title, mode=args.mode),
        encoding="utf-8",
    )
    print(f"\nArtifact written: {args.out}")


if __name__ == "__main__":
    main()
