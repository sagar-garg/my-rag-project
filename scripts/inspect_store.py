"""Peek inside the vector store: what does a stored 'point' actually hold?

Free to run (local read only, no Azure calls). Shows the collection,
a point's id, vector shape, and payload — the raw unit of retrieval.

    .venv/bin/python -m scripts.inspect_store
"""

from __future__ import annotations

from app.clients import build_qdrant_client
from app.config import AppConfig


def main() -> None:
    config = AppConfig.from_env()
    client = build_qdrant_client(config)
    collection = config.qdrant_collection_name

    if not client.collection_exists(collection):
        print(f"Collection `{collection}` does not exist yet. Run build_index first.")
        return

    info = client.get_collection(collection)
    print(f"Collection: {collection}")
    print(f"  points (chunks): {info.points_count}")
    print(f"  vector size:     {info.config.params.vectors.size}")
    print(f"  distance metric: {info.config.params.vectors.distance}")

    points, _ = client.scroll(
        collection_name=collection,
        limit=3,
        with_payload=True,
        with_vectors=True,
    )
    for point in points:
        vector = point.vector or []
        text = str(point.payload.get("text", ""))
        print("\n--- one point (one chunk) ---")
        print(f"  id:          {point.id}")
        print(f"  vector dims: {len(vector)}  first 5: {[round(v, 4) for v in vector[:5]]}")
        print(f"  source:      {point.payload.get('source_path')} | chunk {point.payload.get('chunk_index')}")
        print(f"  text[:200]:  {text[:200]!r}")


if __name__ == "__main__":
    main()
