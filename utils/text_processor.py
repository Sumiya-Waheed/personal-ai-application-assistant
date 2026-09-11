"""Text cleaning and deterministic chunking."""
from __future__ import annotations
import re
from typing import Iterable

def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    text = clean_text(text)
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, current = [], ""
    for para in paragraphs:
        if len(para) <= chunk_size and len(current) + len(para) + 1 <= chunk_size:
            current = f"{current}\n{para}".strip()
            continue
        if current:
            chunks.append(current)
        if len(para) <= chunk_size:
            current = para
        else:
            start = 0
            while start < len(para):
                end = min(start + chunk_size, len(para))
                piece = para[start:end].strip()
                if piece:
                    chunks.append(piece)
                if end == len(para):
                    break
                start = max(0, end - overlap)
            current = ""
    if current:
        chunks.append(current)

    # Add a small overlap between adjacent final chunks when possible.
    result = []
    for i, chunk in enumerate(chunks):
        if i and overlap:
            tail = chunks[i-1][-overlap:]
            chunk = f"{tail}\n{chunk}"
        result.append(chunk[:chunk_size + overlap])
    return result
