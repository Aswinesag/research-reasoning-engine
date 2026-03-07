class Retriever:
    def __init__(self, vector_store, embedder, reranker):
        self.vector_store = vector_store
        self.embedder = embedder
        self.reranker = reranker

    def retrieve(self, query: str, top_k=5):
        query_embedding = self.embedder.embed(query)
        docs = self.vector_store.search(query_embedding, top_k)
        return self.reranker.rank(query, docs)