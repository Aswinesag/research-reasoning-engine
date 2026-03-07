from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INDEX_PATH = Path("data/index/faiss.index")
METADATA_PATH = Path("data/index/metadata.json")


class SearchResult:
    def __init__(self, score, page_content, metadata):
        self.score = score
        self.page_content = page_content
        self.metadata = metadata


class VectorStore:
    def __init__(self):
        print("🔎 Loading FAISS index...")
        self.index = faiss.read_index(str(INDEX_PATH))

        print("📄 Loading metadata...")
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print("🧠 Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            metadata = self.metadata[idx]
            results.append(
                SearchResult(
                    score=float(score),
                    page_content=metadata["text"],
                    metadata={"doc_id": metadata["doc_id"]},
                )
            )

        return results


def load_vector_store():
    return VectorStore()