"""Simple pluggable LLM provider."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from openai import OpenAI, OpenAIError

from ..config import get_settings


@dataclass(frozen=True)
class LLMResult:
    text: str


class LLM(Protocol):
    def generate(self, prompt: str) -> LLMResult:
        ...


class FakeLLM:
    def __init__(self, agent: str) -> None:
        self.agent = agent

    def generate(self, prompt: str) -> LLMResult:
        text = f"[{self.agent.upper()} RESPONSE] {prompt[:200]}"
        return LLMResult(text=text)


class OpenAILLM:
    def __init__(self, *, api_key: str, model: str, organization: str | None) -> None:
        client_kwargs = {"api_key": api_key}
        if organization:
            client_kwargs["organization"] = organization
        self._client = OpenAI(**client_kwargs)
        self._model = model

    def generate(self, prompt: str) -> LLMResult:
        try:
            response = self._client.responses.create(model=self._model, input=prompt)
        except OpenAIError as exc:
            raise RuntimeError("OpenAI request failed") from exc
        text = response.output_text or ""
        return LLMResult(text=text.strip())


def get_llm(agent: str) -> LLM:
    settings = get_settings()
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY must be set when using the OpenAI provider")
        return OpenAILLM(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            organization=settings.openai_organization,
        )
    return FakeLLM(agent)


__all__ = ["LLM", "LLMResult", "FakeLLM", "OpenAILLM", "get_llm"]
