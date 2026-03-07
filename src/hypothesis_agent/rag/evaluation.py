# src/hypothesis_agent/rag/evaluation.py

from __future__ import annotations

from pathlib import Path
from typing import List, Dict
import json
import time

from hypothesis_agent.rag.embedder import Embedder
from hypothesis_agent.rag.vector_store import VectorStore


class RetrievalEvaluator:
    def __init__(self, index_path: Path, metadata_path: Path):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.vector_store.load(index_path, metadata_path)

    def evaluate(self, eval_path: Path, k: int = 5) -> Dict[str, float]:
        with open(eval_path, "r", encoding="utf-8") as f:
            eval_data = json.load(f)

        total = len(eval_data)
        recall_hits = 0
        precision_sum = 0.0
        mrr_sum = 0.0
        total_latency = 0.0

        for item in eval_data:
            query = item["query"]
            relevant = set(item["relevant_doc_ids"])

            start = time.time()
            query_embedding = self.embedder.encode([query])
            results = self.vector_store.search(query_embedding, k=k)
            latency = time.time() - start

            total_latency += latency

            retrieved_doc_ids = [chunk.doc_id for chunk, _ in results]

            # Recall@k
            if any(doc_id in relevant for doc_id in retrieved_doc_ids):
                recall_hits += 1

            # Precision@k
            hits = sum(1 for doc_id in retrieved_doc_ids if doc_id in relevant)
            precision_sum += hits / k

            # MRR
            reciprocal_rank = 0.0
            for rank, doc_id in enumerate(retrieved_doc_ids, start=1):
                if doc_id in relevant:
                    reciprocal_rank = 1.0 / rank
                    break
            mrr_sum += reciprocal_rank

        return {
            "recall@k": recall_hits / total,
            "precision@k": precision_sum / total,
            "MRR": mrr_sum / total,
            "avg_latency_sec": total_latency / total,
        }