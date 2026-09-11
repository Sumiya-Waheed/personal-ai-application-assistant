"""Thin Groq API wrapper with friendly error handling."""
from __future__ import annotations
import json
from groq import Groq
from config import MODEL_NAME, require_groq_api_key

class GroqClient:
    def __init__(self, model: str = MODEL_NAME):
        self.model = model
        self.client = Groq(api_key=require_groq_api_key())

    def complete(self, system: str, user: str, temperature: float = 0.2, max_tokens: int = 1800) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            message = str(exc)
            if "429" in message or "rate" in message.lower():
                raise RuntimeError("The AI service is rate-limited. Please wait briefly and try again.") from exc
            raise RuntimeError(f"Groq request failed: {message}") from exc

    def json_complete(self, system: str, user: str, temperature: float = 0.0, max_tokens: int = 2200) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or "{}"
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("The AI returned an invalid structured response. Please retry.") from exc
        except Exception as exc:
            message = str(exc)
            if "429" in message or "rate" in message.lower():
                raise RuntimeError("The AI service is rate-limited. Please wait briefly and try again.") from exc
            raise RuntimeError(f"Groq structured request failed: {message}") from exc
