"""Pure helpers for the Streamlit retrieval inspector.

No Streamlit imports here — everything is plain-function logic so it can be
unit-tested without a running app.
"""

from __future__ import annotations

from app.eval.basic_eval import StarterEvalCase


def chapter_label(file_name: str) -> str:
    """Compress `Chapter_6_RAG_and_Agents.pdf` to `Ch6` for compact display."""

    parts = file_name.split("_")
    if len(parts) >= 2 and parts[0] == "Chapter":
        return f"Ch{parts[1]}"
    return file_name


def _normalize(question: str) -> str:
    return " ".join(question.split()).casefold()


def find_matching_case(
    question: str, cases: list[StarterEvalCase]
) -> StarterEvalCase | None:
    """Match a typed question against the eval set, tolerating whitespace
    and case differences from copy-paste. Returns None when the question
    is not an eval question."""

    normalized = _normalize(question)
    if not normalized:
        return None
    for case in cases:
        if _normalize(case.question) == normalized:
            return case
    return None


def score_caption(mode: str) -> str:
    """What the score column means — `RetrievedChunk.score` is overloaded
    per retrieval mode, and the rerank path keeps the dense score."""

    captions = {
        "dense": "Score = cosine similarity (dense embedding).",
        "hybrid": "Score = reciprocal rank fusion of dense + BM25 ranks.",
        "rerank": "Score = original dense similarity; order = LLM rerank.",
    }
    if mode not in captions:
        raise ValueError(f"Unknown retrieval mode: {mode!r}")
    return captions[mode]
