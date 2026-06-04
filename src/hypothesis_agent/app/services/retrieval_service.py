import faiss
import numpy as np
import json
import os
from functools import lru_cache
from pathlib import Path
from hypothesis_agent.core.models import EvidenceSnippet


@lru_cache(maxsize=1)
def get_sentence_transformer():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


class RetrievalService:
    def __init__(self):
        self._model = None

        project_root = Path(__file__).resolve().parents[4]

        index_candidates = [
            project_root / "data" / "index" / "faiss.index",
            project_root / "data" / "processed" / "index.faiss",
        ]
        metadata_candidates = [
            project_root / "data" / "index" / "metadata.json",
            project_root / "data" / "processed" / "metadata.json",
        ]

        index_path = next((path for path in index_candidates if path.exists()), None)
        if index_path is None:
            raise FileNotFoundError("No FAISS index found in data/index or data/processed")

        metadata_path = next((path for path in metadata_candidates if path.exists()), None)
        if metadata_path is None:
            raise FileNotFoundError("No metadata.json found in data/index or data/processed")

        self.index = faiss.read_index(str(index_path))

        with metadata_path.open("r", encoding="utf-8") as file:
            self.metadata = json.load(file)

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
