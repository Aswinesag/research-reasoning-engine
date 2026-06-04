import faiss
import numpy as np
import json
import os
from functools import lru_cache
from hypothesis_agent.core.models import EvidenceSnippet


@lru_cache(maxsize=1)
def get_sentence_transformer():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


class RetrievalService:
    def __init__(self):
        self._model = None

        # Get project root (go up from src/hypothesis_agent/app/services)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
        
        # Load FAISS index
        index_path = os.path.join(project_root, "data", "index", "faiss.index")
        self.index = faiss.read_index(index_path)

        # Load metadata JSON
        metadata_path = os.path.join(project_root, "data", "index", "metadata.json")
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print(f"FAISS index loaded with {self.index.ntotal} vectors.")
        print(f"Metadata entries loaded: {len(self.metadata)}")

        # Safety check
        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                "Mismatch between FAISS index size and metadata entries!"
            )

    @property
    def model(self):
        if self._model is None:
            self._model = get_sentence_transformer()
        return self._model

    def search(self, query: str, top_k: int = 5):
        # Embed query
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        # Search
        distances, indices = self.index.search(query_embedding, top_k)

        snippets = []

        for rank, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            meta = self.metadata[idx]

            # Convert FAISS distance → similarity score
            similarity = float(1 / (1 + distances[0][rank]))

            snippet = EvidenceSnippet(
                id=str(idx),
                doc_id=meta.get("doc_id", f"doc_{idx}"),
                text=meta.get("text", ""),
                score=similarity,
            )

            snippets.append(snippet)

        return snippets


# Singleton instance
retrieval_service = RetrievalService()
