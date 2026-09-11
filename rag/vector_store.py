"""FAISS index plus traceable chunk metadata."""
from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np
import faiss

@dataclass
class ChunkRecord:
    text: str
    source: str
    document_type: str
    chunk_id: int
    section: str = ""

class VectorStore:
    def __init__(self):
        self.index = None
        self.records: list[ChunkRecord] = []

    @property
    def is_empty(self) -> bool:
        return not self.records or self.index is None or self.index.ntotal == 0

    def build(self, embeddings: np.ndarray, records: list[ChunkRecord]) -> None:
        if len(records) == 0:
            self.index, self.records = None, []
            return
        if len(embeddings) != len(records):
            raise ValueError("Embedding and metadata counts do not match.")
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(np.ascontiguousarray(embeddings, dtype="float32"))
        self.records = list(records)

    def search(self, query_embedding: np.ndarray, top_k: int = 6) -> list[dict]:
        if self.is_empty:
            return []
        q = np.asarray(query_embedding, dtype="float32")
        if q.ndim == 1:
            q = q.reshape(1, -1)
        scores, indices = self.index.search(q, min(top_k, len(self.records)))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            item = asdict(self.records[int(idx)])
            item["score"] = float(score)
            results.append(item)
        return results
