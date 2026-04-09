from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "docs"
DEFAULT_PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_SOURCE_FILE_NAMES = (
    "Chapter_4_Evaluate_AI_Systems.pdf",
    "Chapter_5_Prompt_Engineering.pdf",
    "Chapter_6_RAG_and_Agents.pdf",
)


@dataclass(frozen=True)
class AppConfig:
    """Application settings loaded from environment variables."""

    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str
    chat_deployment_name: str
    embedding_deployment_name: str
    qdrant_url: str
    qdrant_api_key: str | None
    qdrant_collection_name: str
    raw_data_dir: Path
    processed_data_dir: Path
    source_file_names: tuple[str, ...]
    chunk_size: int
    chunk_overlap: int
    top_k: int
    embedding_batch_size: int

    @classmethod
    def from_env(cls, env_path: Path | None = None) -> "AppConfig":
        """Load configuration from `.env` and process defaults."""

        resolved_env_path = env_path or PROJECT_ROOT / ".env"
        load_dotenv(resolved_env_path if resolved_env_path.exists() else None)

        missing_values = [
            name
            for name in (
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
                "AZURE_OPENAI_API_VERSION",
                "AZURE_OPENAI_CHAT_DEPLOYMENT",
                "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
                "QDRANT_URL",
            )
            if not os.getenv(name)
        ]

        if missing_values:
            missing_text = ", ".join(missing_values)
            raise ValueError(
                "Missing required environment variables: "
                f"{missing_text}. Copy `.env.example` to `.env` and fill them in."
            )

        return cls(
            azure_openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            chat_deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
            embedding_deployment_name=os.environ[
                "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
            ],
            qdrant_url=os.environ["QDRANT_URL"],
            qdrant_api_key=os.getenv("QDRANT_API_KEY"),
            qdrant_collection_name=os.getenv(
                "QDRANT_COLLECTION_NAME",
                "book_chapters_4_6",
            ),
            raw_data_dir=Path(os.getenv("RAW_DATA_DIR", DEFAULT_RAW_DATA_DIR)),
            processed_data_dir=Path(
                os.getenv("PROCESSED_DATA_DIR", DEFAULT_PROCESSED_DATA_DIR)
            ),
            source_file_names=_read_csv_from_env(
                "SOURCE_FILE_NAMES",
                DEFAULT_SOURCE_FILE_NAMES,
            ),
            chunk_size=_read_int_from_env("CHUNK_SIZE", 512),
            chunk_overlap=_read_int_from_env("CHUNK_OVERLAP", 80),
            top_k=_read_int_from_env("TOP_K", 4),
            embedding_batch_size=_read_int_from_env("EMBEDDING_BATCH_SIZE", 16),
        )


def _read_int_from_env(name: str, default_value: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default_value

    try:
        return int(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"Environment variable `{name}` must be an integer, got `{raw_value}`."
        ) from exc


def _read_csv_from_env(
    name: str,
    default_values: tuple[str, ...],
) -> tuple[str, ...]:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default_values

    values = tuple(
        item.strip()
        for item in raw_value.split(",")
        if item.strip()
    )
    if not values:
        raise ValueError(
            f"Environment variable `{name}` must contain at least one comma-separated value."
        )
    return values
