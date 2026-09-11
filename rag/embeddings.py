"""Sentence Transformer embedding service."""
from __future__ import annotations
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingService:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 0), dtype="float32")
        vectors = self.model.encode(
            texts, convert_to_numpy=True, normalize_embeddings=True,
            show_progress_bar=False
        )
        return np.asarray(vectors, dtype="float32")
