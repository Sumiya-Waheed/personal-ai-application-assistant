"""High-level LLM generation services."""
from __future__ import annotations
from llm.groq_client import GroqClient
from llm import prompts

def _evidence_block(evidence: list[dict]) -> str:
    if not evidence:
        return "No profile evidence was retrieved."
    return "\n\n".join(
        f"[{i+1}] {e['source']} | {e.get('section') or 'General'} | score={e['score']:.3f}\n{e['text']}"
        for i, e in enumerate(evidence)
    )

def analyze_opportunity(client: GroqClient, opportunity_text: str) -> dict:
    return client.json_complete(prompts.OPPORTUNITY_SYSTEM, opportunity_text, max_tokens=2500)

def match_profile(client: GroqClient, analysis: dict, evidence: list[dict]) -> dict:
    user = "OPPORTUNITY ANALYSIS:\n" + str(analysis) + "\n\nPROFILE EVIDENCE:\n" + _evidence_block(evidence)
    return client.json_complete(prompts.MATCH_SYSTEM, user, max_tokens=2800)

def answer_application_question(client: GroqClient, question: str, opportunity: str, evidence: list[dict]) -> str:
    user = f"QUESTION:\n{question}\n\nOPPORTUNITY CONTEXT:\n{opportunity}\n\nPROFILE EVIDENCE:\n{_evidence_block(evidence)}"
    return client.complete(prompts.ANSWER_SYSTEM, user, temperature=0.25, max_tokens=1200)

def tailor_resume(client: GroqClient, opportunity: str, evidence: list[dict]) -> str:
    user = f"OPPORTUNITY:\n{opportunity}\n\nPROFILE EVIDENCE:\n{_evidence_block(evidence)}"
    return client.complete(prompts.RESUME_SYSTEM, user, temperature=0.2, max_tokens=2600)

def refine_answer(client: GroqClient, original: str, instruction: str, evidence: list[dict]) -> str:
    user = f"ORIGINAL ANSWER:\n{original}\n\nREVISION INSTRUCTION:\n{instruction}\n\nAVAILABLE EVIDENCE:\n{_evidence_block(evidence)}"
    return client.complete(prompts.REFINE_SYSTEM, user, temperature=0.2, max_tokens=1200)
