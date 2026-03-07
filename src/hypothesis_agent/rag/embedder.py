from __future__ import annotations

from typing import List
import torch
from sentence_transformers import SentenceTransformer

class Embedder:
    """
    GPU-backed embedding wrapper.
    Deterministic and production-safe.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Deterministic settings
        torch.manual_seed(42)
        torch.cuda.manual_seed_all(42)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        self.model = SentenceTransformer(model_name, device=self.device)
    
    def encode(self, texts: List[str], batch_size: int = 32) -> torch.Tensor:
        """
        Returns embeddings as float32 tensor on CPU (for FAISS compatibility).
        """

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_tensor=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        # Move to CPU for FAISS
        return embeddings.detach().cpu().float()