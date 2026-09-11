"""Retrieval facade; consumers never touch FAISS directly."""
from __future__ import annotations
from rag.embeddings import EmbeddingService
from rag.vector_store import VectorStore

class Retriever:
    def __init__(self, store: VectorStore, embeddings: EmbeddingService):
        self.store = store
        self.embeddings = embeddings

    def retrieve(self, query: str, top_k: int = 6) -> list[dict]:
        if not query.strip() or self.store.is_empty:
            return []
        q = self.embeddings.encode([query])
        return self.store.search(q, top_k=top_k)
