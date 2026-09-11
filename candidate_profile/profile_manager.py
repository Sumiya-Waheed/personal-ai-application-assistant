"""Build and manage the in-session personal knowledge base."""
from __future__ import annotations
from dataclasses import dataclass
from rag.vector_store import VectorStore, ChunkRecord
from rag.embeddings import EmbeddingService
from utils.file_parser import extract_text
from utils.text_processor import clean_text, chunk_text
from config import CHUNK_SIZE, CHUNK_OVERLAP

@dataclass
class ProcessedDocument:
    filename: str
    document_type: str
    chunks: int

class ProfileManager:
    def __init__(self, embeddings: EmbeddingService):
        self.embeddings = embeddings
        self.store = VectorStore()
        self.documents: list[ProcessedDocument] = []

    def rebuild(self, uploaded_files) -> list[ProcessedDocument]:
        records: list[ChunkRecord] = []
        docs: list[ProcessedDocument] = []
        for uploaded in uploaded_files:
            text = clean_text(extract_text(uploaded.name, uploaded.getvalue()))
            chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            if not chunks:
                raise ValueError(f"No usable text remained after processing '{uploaded.name}'.")
            document_type = uploaded.name.rsplit(".", 1)[-1].upper()
            for i, chunk in enumerate(chunks):
                records.append(ChunkRecord(
                    text=chunk, source=uploaded.name, document_type=document_type,
                    chunk_id=i, section=""
                ))
            docs.append(ProcessedDocument(uploaded.name, document_type, len(chunks)))
        embeddings = self.embeddings.encode([r.text for r in records])
        self.store.build(embeddings, records)
        self.documents = docs
        return docs

    def stats(self) -> dict:
        return {"documents": len(self.documents), "chunks": len(self.store.records)}
