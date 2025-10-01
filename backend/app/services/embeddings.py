"""Embedding provider interface and fake implementation."""
from __future__ import annotations

import hashlib
from typing import Iterable, Protocol


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> list[float]:
        ...


class FakeEmbeddingProvider:
    """Deterministic embedding provider for offline demos."""

    def embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Generate 16 pseudo-random floats between -1 and 1
        return [((byte / 255.0) * 2) - 1 for byte in digest[:16]]


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    import math

    a_list = list(a)
    b_list = list(b)
    if not a_list or not b_list:
        return 0.0
    dot = sum(x * y for x, y in zip(a_list, b_list))
    norm_a = math.sqrt(sum(x * x for x in a_list))
    norm_b = math.sqrt(sum(x * x for x in b_list))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


__all__ = ["EmbeddingProvider", "FakeEmbeddingProvider", "cosine_similarity"]
