from pathlib import Path

def test_index_persistence(tmp_path):
    from hypothesis_agent.rag.embedder import Embedder
    from hypothesis_agent.rag.document_store import DocumentStore
    from hypothesis_agent.rag.vector_store import VectorStore

    store = DocumentStore(Path("data/raw/corpus.json"))
    chunks = store.load()

    embedder = Embedder()
    embeddings = embedder.encode([c.text for c in chunks])

    vector_store = VectorStore(dim=384)
    vector_store.build(embeddings, chunks)

    index_path = tmp_path / "index.faiss"
    meta_path = tmp_path / "meta.json"

    vector_store.save(index_path, meta_path)

    # Load into new instance
    new_store = VectorStore(dim=384)
    new_store.load(index_path, meta_path)

    query_embedding = embedder.encode(["immune genome editing"])
    results = new_store.search(query_embedding, k=1)

    assert len(results) > 0