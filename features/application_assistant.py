"""Application Q&A orchestration."""
from __future__ import annotations
from config import TOP_K
from llm.generator import answer_application_question, refine_answer

class ApplicationAssistant:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def answer(self, question: str, opportunity: str) -> tuple[str, list[dict]]:
        evidence = self.retriever.retrieve(question, TOP_K)
        answer = answer_application_question(self.llm, question, opportunity, evidence)
        return answer, evidence

    def refine(self, original: str, instruction: str) -> tuple[str, list[dict]]:
        evidence = self.retriever.retrieve(original, TOP_K)
        answer = refine_answer(self.llm, original, instruction, evidence)
        return answer, evidence
