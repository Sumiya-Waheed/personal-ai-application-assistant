"""Profile ↔ opportunity matching service."""
from __future__ import annotations
from config import TOP_K
from llm.generator import match_profile

class OpportunityMatcher:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def retrieve_for_analysis(self, analysis: dict, top_k: int = TOP_K) -> list[dict]:
        queries = []
        for key in ("eligibility_requirements", "education_requirements", "required_skills",
                    "required_experience", "preferred_qualifications", "documents_required", "important_criteria"):
            queries.extend(analysis.get(key, [])[:4])
        query = " ".join(queries) or str(analysis)
        return self.retriever.retrieve(query, top_k=top_k)

    def match(self, analysis: dict, evidence: list[dict]) -> dict:
        return match_profile(self.llm, analysis, evidence)
