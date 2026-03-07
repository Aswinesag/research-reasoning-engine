import json
from pathlib import Path
from typing import List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 256


def load_corpus(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def chunk_text(text: str, tokenizer, chunk_size: int = 256):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []

    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks


def main():
    corpus_path = Path("data/raw/corpus.json")
    index_path = Path("data/index/faiss.index")
    metadata_path = Path("data/index/metadata.json")

    corpus = load_corpus(corpus_path)

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    all_chunks: List[str] = []
    metadata = []

    print("Chunking documents...")

    for doc in corpus:
        combined = f"{doc['title']} {doc['abstract']}"
        chunks = chunk_text(combined, tokenizer, CHUNK_SIZE)

        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "doc_id": doc["id"],
                "text": chunk
            })

    print(f"Total chunks: {len(all_chunks)}")

    print("Generating embeddings...")
    embeddings = model.encode(
        all_chunks,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    dimension = embeddings.shape[1]
    print(f"Embedding dimension: {dimension}")

    index = faiss.IndexFlatIP(dimension)  # cosine similarity (after normalization)
    index.add(embeddings)

    index_path.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(index_path))

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    print("Index saved successfully.")


if __name__ == "__main__":
    main()