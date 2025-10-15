"""Simple pluggable LLM provider."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

from openai import OpenAI, OpenAIError

from ..config import get_settings

logger = logging.getLogger(__name__)


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
        self._api_key = api_key
        self._model = model
        self._organization = organization or None
        self._client = self._build_client()

    def _build_client(self) -> OpenAI:
        client_kwargs = {"api_key": self._api_key}
        if self._organization:
            client_kwargs["organization"] = self._organization
        logger.info(
            "Initializing OpenAI client",
            extra={"model": self._model, "organization": self._organization or "<none>"},
        )
        return OpenAI(**client_kwargs)

    @staticmethod
    def _is_invalid_organization_error(exc: OpenAIError) -> bool:
        code = getattr(exc, "code", None)
        if isinstance(code, str) and code == "invalid_organization":
            return True
        message = getattr(exc, "message", "") or str(exc)
        return "invalid_organization" in message

    def generate(self, prompt: str) -> LLMResult:
        return self._generate(prompt, allow_retry=True)

    def _generate(self, prompt: str, *, allow_retry: bool) -> LLMResult:
        try:
            response = self._client.responses.create(model=self._model, input=prompt)
        except OpenAIError as exc:
            logger.error(
                "OpenAI request failed",
                exc_info=exc,
                extra={"model": self._model, "organization": self._organization or "<none>"},
            )
            if allow_retry and self._organization and self._is_invalid_organization_error(exc):
                logger.warning(
                    "OpenAI reported invalid organization. Retrying without organization header.",
                    extra={"organization": self._organization},
                )
                self._organization = None
                self._client = self._build_client()
                return self._generate(prompt, allow_retry=False)
            raise RuntimeError("OpenAI request failed") from exc
        text = response.output_text or ""
        return LLMResult(text=text.strip())


def get_llm(agent: str) -> LLM:
    settings = get_settings()
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY must be set when using the OpenAI provider")
        logger.info(
            "Using OpenAI provider",
            extra={
                "agent": agent,
                "model": settings.openai_model,
                "organization": settings.openai_organization or "<none>",
            },
        )
        return OpenAILLM(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            organization=settings.openai_organization,
        )
    return FakeLLM(agent)


__all__ = ["LLM", "LLMResult", "FakeLLM", "OpenAILLM", "get_llm"]
