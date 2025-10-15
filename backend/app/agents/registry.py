"""Agent registry mapping identifiers to factories."""
from __future__ import annotations

from typing import Callable, Dict

from . import accountant, copywriter, marketing, support
from .base import AgentContext

_REGISTRY: Dict[str, Callable[[], AgentContext]] = {
    "accountant": accountant.get_agent,
    "support": support.get_agent,
    "copywriter": copywriter.get_agent,
    "marketing": marketing.get_agent,
}


def get_agent(agent_id: str) -> AgentContext:
    try:
        return _REGISTRY[agent_id]()
    except KeyError as exc:
        raise ValueError(f"Unknown agent: {agent_id}") from exc


__all__ = ["get_agent"]
