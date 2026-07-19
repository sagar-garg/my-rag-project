import types

from app.models import RetrievedChunk
from app.retrieval.rerank import (
    build_rerank_prompt,
    parse_ranking,
    rerank_chunks,
)


_STUB_CONFIG = types.SimpleNamespace(chat_deployment_name="fake-chat-deployment")


def _make_chunks(count: int) -> list[RetrievedChunk]:
    return [
        RetrievedChunk(
            chunk_id=f"chunk-{index}",
            text=f"Passage text number {index}.",
            source_path=f"notes/doc-{index}.md",
            file_name=f"doc-{index}.md",
            chunk_index=index,
            score=1.0 - index * 0.1,
        )
        for index in range(1, count + 1)
    ]


def test_build_rerank_prompt_includes_question_and_numbered_blocks_without_sources() -> None:
    chunks = _make_chunks(2)

    prompt = build_rerank_prompt("What is chunk overlap?", chunks)

    assert "What is chunk overlap?" in prompt
    assert "[1]" in prompt
    assert "[2]" in prompt
    assert "Passage text number 1." in prompt
    assert "Passage text number 2." in prompt
    assert "notes/doc-1.md" not in prompt
    assert "notes/doc-2.md" not in prompt


def test_parse_ranking_json_array() -> None:
    assert parse_ranking("[3, 1, 2]", 3) == [3, 1, 2]


def test_parse_ranking_prose() -> None:
    assert parse_ranking("Ranking: 2, 1, 3.", 3) == [2, 1, 3]


def test_parse_ranking_dedupes_to_first_occurrence() -> None:
    assert parse_ranking("[2, 2, 1, 2]", 2) == [2, 1]


def test_parse_ranking_drops_out_of_range_values() -> None:
    assert parse_ranking("[0, 3, 1, 4]", 3) == [3, 1, 2]


def test_parse_ranking_appends_missing_indices_ascending() -> None:
    assert parse_ranking("[2]", 4) == [2, 1, 3, 4]


def test_parse_ranking_falls_back_to_identity_on_garbage() -> None:
    assert parse_ranking("no digits here at all", 3) == [1, 2, 3]


class _StubResponses:
    def __init__(self, output_text: str, input_tokens: int, output_tokens: int) -> None:
        self._output_text = output_text
        self._usage = types.SimpleNamespace(
            input_tokens=input_tokens, output_tokens=output_tokens
        )
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return types.SimpleNamespace(
            output_text=self._output_text,
            usage=self._usage,
        )


class _StubAzureClient:
    def __init__(self, output_text: str, input_tokens: int = 12, output_tokens: int = 4) -> None:
        self.responses = _StubResponses(output_text, input_tokens, output_tokens)


def test_rerank_chunks_reorders_truncates_and_surfaces_token_counts() -> None:
    chunks = _make_chunks(2)
    stub_client = _StubAzureClient("[2, 1]", input_tokens=12, output_tokens=4)

    result = rerank_chunks(
        "question",
        chunks,
        config=_STUB_CONFIG,
        top_k=1,
        azure_client=stub_client,
    )

    assert [chunk.chunk_id for chunk in result.chunks] == ["chunk-2"]
    assert result.input_tokens == 12
    assert result.output_tokens == 4
    assert len(stub_client.responses.calls) == 1


def test_rerank_chunks_empty_candidates_returns_empty_result_without_calling_api() -> None:
    stub_client = _StubAzureClient("[]")

    result = rerank_chunks(
        "question",
        [],
        config=_STUB_CONFIG,
        top_k=3,
        azure_client=stub_client,
    )

    assert result.chunks == []
    assert result.input_tokens == 0
    assert result.output_tokens == 0
    assert stub_client.responses.calls == []
