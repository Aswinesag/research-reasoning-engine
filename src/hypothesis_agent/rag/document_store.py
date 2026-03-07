# src/hypothesis_agent/rag/document_store.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List
import json
import re
from pathlib import Path


@dataclass(frozen=True)
class DocumentChunk:
    doc_id: str
    chunk_id: str
    text: str


class DocumentStore:
    """
    Loads corpus and produces deterministic 256-token chunks.
    """

    def __init__(self, corpus_path: Path, chunk_size: int = 256) -> None:
        self.corpus_path = corpus_path
        self.chunk_size = chunk_size

    def load(self) -> List[DocumentChunk]:
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks: List[DocumentChunk] = []

        for doc in data:
            base_id = doc["id"]

            # Deterministic normalization
            title = self._clean_text(doc["title"])
            abstract = self._clean_text(doc["abstract"])

            full_text = f"{title}. {abstract}"

            token_chunks = self._chunk_text(full_text)

            for idx, chunk in enumerate(token_chunks):
                chunks.append(
                    DocumentChunk(
                        doc_id=base_id,
                        chunk_id=f"{base_id}_chunk_{idx}",
                        text=chunk,
                    )
                )

        return chunks

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text.strip())
        return text

    def _chunk_text(self, text: str) -> List[str]:
        tokens = text.split(" ")
        chunks = []

        for i in range(0, len(tokens), self.chunk_size):
            chunk_tokens = tokens[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_tokens)
            chunks.append(chunk_text)

        return chunks