from pathlib import Path
import time

from hypothesis_agent.rag.embedder import Embedder
from hypothesis_agent.rag.document_store import DocumentStore
from hypothesis_agent.rag.vector_store import VectorStore


def main() -> None:
    raw_path = Path("data/raw/corpus.json")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    index_path = processed_dir / "index.faiss"
    metadata_path = processed_dir / "metadata.json"

    print("Loading corpus...")
    store = DocumentStore(raw_path)
    chunks = store.load()
    print(f"Loaded {len(chunks)} chunks")

    print("Embedding...")
    start = time.time()
    embedder = Embedder()
    embeddings = embedder.encode([c.text for c in chunks])
    embed_time = time.time() - start
    print(f"Embedding complete in {embed_time:.2f}s")

    print("Building FAISS index...")
    vector_store = VectorStore(dim=embeddings.shape[1])
    vector_store.build(embeddings, chunks)

    print("Saving index...")
    vector_store.save(index_path, metadata_path)

    print("Index build complete.")
    print(f"Index saved to: {index_path}")
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()