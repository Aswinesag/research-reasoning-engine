def test_rag_pipeline():
    from pathlib import Path

    from hypothesis_agent.rag.embedder import Embedder
    from hypothesis_agent.rag.document_store import DocumentStore
    from hypothesis_agent.rag.vector_store import VectorStore

    store = DocumentStore(Path("data/raw/corpus.json"))
    chunks = store.load()

    assert len(chunks) > 0

    embedder = Embedder()
    embeddings = embedder.encode([c.text for c in chunks])

    assert embeddings.shape[0] == len(chunks)
    assert embeddings.shape[1] == 384

    vector_store = VectorStore(dim=384)
    vector_store.build(embeddings, chunks)

    query = "immune genome editing"
    query_embedding = embedder.encode([query])
    results = vector_store.search(query_embedding, k=1)

    assert len(results) > 0