"""Tailored resume orchestration."""
from __future__ import annotations
from config import TOP_K
from llm.generator import tailor_resume

class ResumeGenerator:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def generate(self, opportunity: str) -> tuple[str, list[dict]]:
        evidence = self.retriever.retrieve(opportunity, TOP_K)
        resume = tailor_resume(self.llm, opportunity, evidence)
        return resume, evidence
