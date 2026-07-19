"""In-memory BM25 (Okapi) index over the chunk corpus.

The lexical side of hybrid retrieval. Built by scrolling the existing Qdrant
collection — no re-indexing, no API calls, pure local computation.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from qdrant_client import QdrantClient

from app.models import RetrievedChunk

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

_SCROLL_BATCH_SIZE = 256


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens. No stopword list — BM25's IDF already
    downweights terms that appear in most documents."""

    return _TOKEN_PATTERN.findall(text.lower())


class Bm25Index:
    """Okapi BM25 over a fixed list of chunks.

    idf(t) = ln((N - df + 0.5) / (df + 0.5) + 1)
    score(d) = sum over query terms of
        idf(t) * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg_len))
    """

    def __init__(
        self,
        chunks: list[RetrievedChunk],
        *,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        if not chunks:
            raise ValueError("Cannot build a BM25 index from an empty corpus.")

        self.chunks = chunks
        self.k1 = k1
        self.b = b

        self._term_frequencies = [Counter(tokenize(chunk.text)) for chunk in chunks]
        self._doc_lengths = [
            sum(frequencies.values()) for frequencies in self._term_frequencies
        ]
        self._average_doc_length = sum(self._doc_lengths) / len(chunks)

        document_frequencies: Counter[str] = Counter()
        for frequencies in self._term_frequencies:
            document_frequencies.update(frequencies.keys())
        corpus_size = len(chunks)
        self._idf = {
            term: math.log((corpus_size - df + 0.5) / (df + 0.5) + 1)
            for term, df in document_frequencies.items()
        }

    def score(self, question: str) -> list[float]:
        """BM25 score of every chunk in the corpus against the question."""

        query_terms = tokenize(question)
        scores = [0.0] * len(self.chunks)
        for doc_index, frequencies in enumerate(self._term_frequencies):
            length_norm = 1 - self.b + self.b * (
                self._doc_lengths[doc_index] / self._average_doc_length
            )
            for term in query_terms:
                term_frequency = frequencies.get(term, 0)
                if term_frequency == 0:
                    continue
                scores[doc_index] += (
                    self._idf[term]
                    * term_frequency
                    * (self.k1 + 1)
                    / (term_frequency + self.k1 * length_norm)
                )
        return scores

    def search(self, question: str, *, top_k: int) -> list[RetrievedChunk]:
        """Top-k chunks by BM25 score, descending. Chunks scoring 0 (no query
        term overlap) are excluded — they carry no lexical signal."""

        scores = self.score(question)
        ranked_indices = sorted(
            (index for index, score in enumerate(scores) if score > 0),
            key=lambda index: (-scores[index], self.chunks[index].chunk_id),
        )
        return [
            RetrievedChunk(
                chunk_id=self.chunks[index].chunk_id,
                text=self.chunks[index].text,
                source_path=self.chunks[index].source_path,
                file_name=self.chunks[index].file_name,
                chunk_index=self.chunks[index].chunk_index,
                score=scores[index],
            )
            for index in ranked_indices[:top_k]
        ]


def load_corpus(client: QdrantClient, collection_name: str) -> list[RetrievedChunk]:
    """Fetch every chunk payload from the collection via paginated scroll."""

    corpus: list[RetrievedChunk] = []
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=collection_name,
            limit=_SCROLL_BATCH_SIZE,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for point in points:
            payload = point.payload or {}
            corpus.append(
                RetrievedChunk(
                    chunk_id=str(point.id),
                    text=str(payload.get("text", "")),
                    source_path=str(payload.get("source_path", "unknown")),
                    file_name=str(payload.get("file_name", "unknown")),
                    chunk_index=int(payload.get("chunk_index", 0)),
                    score=0.0,
                )
            )
        if offset is None:
            return corpus
