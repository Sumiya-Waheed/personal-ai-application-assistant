"""Opportunity analysis service."""
from __future__ import annotations
from llm.generator import analyze_opportunity

class OpportunityAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def analyze(self, text: str) -> dict:
        if not text.strip():
            raise ValueError("The opportunity document contains no usable text.")
        return analyze_opportunity(self.llm, text)
