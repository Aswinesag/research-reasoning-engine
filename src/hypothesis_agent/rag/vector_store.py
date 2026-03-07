# src/hypothesis_agent/rag/vector_store.py

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import json
import numpy as np
import faiss
import torch

from hypothesis_agent.rag.document_store import DocumentChunk


class VectorStore:
    """
    FAISS-based cosine similarity index.
    """

    def __init__(self, dim: int = 384) -> None:
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[DocumentChunk] = []

    def build(self, embeddings: torch.Tensor, chunks: List[DocumentChunk]) -> None:
        """
        Build FAISS index from embeddings.
        """

        if embeddings.shape[0] != len(chunks):
            raise ValueError("Embeddings and chunks length mismatch.")

        vectors = embeddings.numpy().astype(np.float32)

        self.index.add(vectors)
        self.metadata = chunks

    def save(self, index_path: Path, metadata_path: Path) -> None:
        faiss.write_index(self.index, str(index_path))

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {
                        "doc_id": c.doc_id,
                        "chunk_id": c.chunk_id,
                        "text": c.text,
                    }
                    for c in self.metadata
                ],
                f,
                indent=2,
            )

    def load(self, index_path: Path, metadata_path: Path) -> None:
        self.index = faiss.read_index(str(index_path))

        with open(metadata_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        self.metadata = [
            DocumentChunk(
                doc_id=item["doc_id"],
                chunk_id=item["chunk_id"],
                text=item["text"],
            )
            for item in raw
        ]

    def search(self, query_embedding: torch.Tensor, k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """
        Returns top-k chunks with similarity score.
        """

        query_vector = query_embedding.numpy().astype(np.float32)

        scores, indices = self.index.search(query_vector, k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue
            results.append((self.metadata[idx], float(score)))

        return results