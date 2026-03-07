import numpy as np
import os
from typing import List
from hypothesis_agent.core.models import EvidenceSnippet

TOP_K = 5
SIMILARITY_THRESHOLD = 0.75

class RetrievalEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def search(self, query: str) -> List[EvidenceSnippet]:
        """
        Retrieve top-k evidence snippets above similarity threshold.
        """

        results = self.vector_store.search(query, top_k=TOP_K)

        filtered = [
            EvidenceSnippet(
                id=i,
                doc_id=r.metadata.get("doc_id", "unknown"),
                text=r.page_content,
                score=float(r.score),
            )
            for i, r in enumerate(results)
            if r.score >= SIMILARITY_THRESHOLD
        ]

        if len(filtered) < 2:
            print("⚠ Warning: Fewer than 2 strong evidence snippets retrieved.")

        return filtered


def main():
    print("🔎 Initializing Retrieval Engine...")

    # You must replace this with your actual vector store loader
    from hypothesis_agent.reasoning.generate import HypothesisGenerator
    from hypothesis_agent.index.vector_store import load_vector_store
    vector_store = load_vector_store()

    retriever = RetrievalEngine(vector_store)

    query = input("Enter research query: ")

    snippets = retriever.search(query)

    print("\nTop Evidence Snippets:")
    for s in snippets:
        print(f"[ID: {s.id}] (Score: {s.score:.3f}) {s.text[:120]}...")

    if not snippets:
        print("No strong evidence found. Exiting.")
        return

    print("\n🧠 Generating Research-Grade Hypothesis...\n")

    generator = HypothesisGenerator()

    result = generator.generate(query, snippets)

    print("\n================ HYPOTHESIS OUTPUT ================\n")
    print(result)
    print("\n===================================================\n")


if __name__ == "__main__":
    main()