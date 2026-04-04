from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    text: str
    source_path: str
    file_name: str
    chunk_index: int
    score: float
