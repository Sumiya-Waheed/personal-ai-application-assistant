"""Transparent, deterministic readiness estimate."""
from __future__ import annotations

CATEGORIES = ("eligibility", "skills", "experience", "documents", "other")

def calculate_readiness(match_result: dict) -> tuple[int, dict[str, int]]:
    raw = match_result.get("category_scores", {})
    scores = {}
    for category in CATEGORIES:
        try:
            scores[category] = max(0, min(100, int(float(raw.get(category, 0)))))
        except (TypeError, ValueError):
            scores[category] = 0
    # Equal-weight average makes the estimate transparent rather than arbitrary.
    overall = round(sum(scores.values()) / len(CATEGORIES))
    return overall, scores
