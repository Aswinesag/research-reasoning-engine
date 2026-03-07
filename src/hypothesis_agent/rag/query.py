from pathlib import Path

from hypothesis_agent.rag.embedder import Embedder
from hypothesis_agent.rag.vector_store import VectorStore


def main() -> None:
    index_path = Path("data/processed/index.faiss")
    metadata_path = Path("data/processed/metadata.json")

    if not index_path.exists():
        print("Index not found. Run build_index first.")
        return

    vector_store = VectorStore()
    vector_store.load(index_path, metadata_path)

    embedder = Embedder()

    query = input("Enter query: ")
    query_embedding = embedder.encode([query])

    results = vector_store.search(query_embedding, k=3)

    print("\nTop Results:\n")
    for chunk, score in results:
        print(f"[Score: {score:.4f}] {chunk.chunk_id}")
        print(chunk.text[:300])
        print("-" * 80)


if __name__ == "__main__":
    main()