"""Base agent wrapper."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from ..graph.builders import AgentRunResult, AgentGraph, build_agent_graph
from ..graph.memory import get_or_create_channel, get_or_create_user


@dataclass
class AgentContext:
    agent: str
    graph: AgentGraph

    def run(self, db: Session, *, text: str, channel_ref: str, user_ref: str, platform: str = "web") -> AgentRunResult:
        channel = get_or_create_channel(db, channel_ref, channel_ref, platform)
        user = get_or_create_user(db, user_ref, user_ref)
        return self.graph.run(db, text=text, channel=channel, user=user)


def create_agent(agent: str) -> AgentContext:
    graph = build_agent_graph(agent)
    return AgentContext(agent=agent, graph=graph)


__all__ = ["AgentContext", "create_agent"]
