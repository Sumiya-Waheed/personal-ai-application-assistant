"""Evidence formatting and source deduplication."""
from __future__ import annotations

def unique_sources(evidence: list[dict]) -> list[dict]:
    seen = set()
    output = []
    for item in evidence:
        key = (item.get("source"), item.get("section"), item.get("chunk_id"))
        if key not in seen:
            seen.add(key)
            output.append(item)
    return output

def source_labels(evidence: list[dict]) -> list[str]:
    return [f"{e.get('source')} — {e.get('section') or 'Relevant excerpt'}" for e in unique_sources(evidence)]
