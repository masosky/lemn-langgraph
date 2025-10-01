"""Support agent factory."""
from __future__ import annotations

from .base import AgentContext, create_agent


def get_agent() -> AgentContext:
    return create_agent("support")


__all__ = ["get_agent"]
