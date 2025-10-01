"""Simple pluggable LLM provider."""
from __future__ import annotations

from dataclasses import dataclass

from ..config import get_settings


@dataclass
class LLMResult:
    text: str


class FakeLLM:
    def __init__(self, agent: str) -> None:
        self.agent = agent

    def generate(self, prompt: str) -> LLMResult:
        text = f"[{self.agent.upper()} RESPONSE] {prompt[:200]}"
        return LLMResult(text=text)


def get_llm(agent: str) -> FakeLLM:
    settings = get_settings()
    if settings.llm_provider == "fake":
        return FakeLLM(agent)
    # For simplicity we return FakeLLM even for other providers in this demo.
    return FakeLLM(agent)


__all__ = ["LLMResult", "FakeLLM", "get_llm"]
