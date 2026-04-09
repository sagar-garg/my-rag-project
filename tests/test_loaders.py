from pathlib import Path

from app.ingest.loaders import load_source_documents


def test_load_source_documents_filters_to_allowed_file_names(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "keep.txt").write_text("Keep this file.", encoding="utf-8")
    (docs_dir / "skip.txt").write_text("Skip this file.", encoding="utf-8")

    documents = load_source_documents(
        docs_dir,
        allowed_file_names={"keep.txt"},
    )

    assert len(documents) == 1
    assert documents[0].metadata["file_name"] == "keep.txt"
    assert documents[0].metadata["source_path"] == "keep.txt"
