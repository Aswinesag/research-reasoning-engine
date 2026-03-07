from pathlib import Path
from hypothesis_agent.rag.evaluation import RetrievalEvaluator


def main():
    index_path = Path("data/processed/index.faiss")
    metadata_path = Path("data/processed/metadata.json")
    eval_path = Path("data/raw/eval_queries.json")

    evaluator = RetrievalEvaluator(index_path, metadata_path)

    metrics = evaluator.evaluate(eval_path, k=3)

    print("\nEvaluation Results:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")


if __name__ == "__main__":
    main()