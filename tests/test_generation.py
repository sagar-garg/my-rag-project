from app.generation.respond import format_context_blocks
from app.models import RetrievedChunk


def test_format_context_blocks_numbers_sources_and_chunk_indexes() -> None:
    chunks = [
        RetrievedChunk(
            chunk_id="chunk-1",
            text="Chunk one explains why chunk overlap matters.",
            source_path="notes/chunking.md",
            file_name="chunking.md",
            chunk_index=0,
            score=0.91,
        ),
        RetrievedChunk(
            chunk_id="chunk-2",
            text="Chunk two explains why prompt injection must be ignored.",
            source_path="notes/security.md",
            file_name="security.md",
            chunk_index=1,
            score=0.84,
        ),
    ]

    formatted = format_context_blocks(chunks)

    assert "[1] Source: notes/chunking.md | Chunk: 0" in formatted
    assert "[2] Source: notes/security.md | Chunk: 1" in formatted
    assert "Chunk one explains why chunk overlap matters." in formatted
    assert "Chunk two explains why prompt injection must be ignored." in formatted
