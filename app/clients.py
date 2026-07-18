from __future__ import annotations

from typing import Any

from openai import AzureOpenAI
from qdrant_client import QdrantClient

from app.config import AppConfig


def build_azure_openai_client(config: AppConfig) -> AzureOpenAI:
    """Create a single Azure OpenAI client from app config."""

    return AzureOpenAI(
        api_key=config.azure_openai_api_key,
        api_version=config.azure_openai_api_version,
        azure_endpoint=config.azure_openai_endpoint,
    )


def build_qdrant_client(config: AppConfig) -> QdrantClient:
    """Create the Qdrant client used for indexing and retrieval.

    Uses a local embedded store (a folder on disk) when
    `qdrant_local_path` is set; otherwise connects to Qdrant Cloud.
    """

    if config.qdrant_local_path:
        return QdrantClient(path=config.qdrant_local_path)

    return QdrantClient(
        url=config.qdrant_url,
        api_key=config.qdrant_api_key,
    )


def embed_texts(
    texts: list[str],
    *,
    config: AppConfig,
    client: AzureOpenAI | None = None,
) -> list[list[float]]:
    """Embed a batch of texts with the Azure OpenAI embedding deployment."""

    if not texts:
        return []

    azure_client = client or build_azure_openai_client(config)
    response = azure_client.embeddings.create(
        model=config.embedding_deployment_name,
        input=texts,
    )

    ordered_rows: list[Any] = sorted(response.data, key=lambda row: row.index)
    return [row.embedding for row in ordered_rows]
