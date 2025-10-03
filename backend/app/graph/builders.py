"""Agent graph builders (simplified LangGraph-like orchestration)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.orm import Session

from ..graph import memory as memory_utils
from ..services.llm import get_llm
from . import tools


@dataclass
class AgentRunResult:
    reply: str
    tool_runs: list[dict[str, Any]] = field(default_factory=list)
    citations: list[dict[str, str]] = field(default_factory=list)


class AgentGraph:
    def __init__(self, agent: str) -> None:
        self.agent = agent

    def run(
        self,
        db: Session,
        *,
        text: str,
        channel,
        user,
    ) -> AgentRunResult:
        recent_messages = memory_utils.fetch_recent_messages(
            db, self.agent, channel.id, user.id if user else None
        )
        context = "\n".join(message.text for message in reversed(recent_messages))
        docs = tools.vector_search(db, text, k=3)
        citations: list[dict[str, Any]] = []
        for doc in docs:
            score = doc["score"] if "score" in doc else 0.0
            citations.append({"title": doc["title"], "score": score})
        prompt_parts = [
            f"Agent: {self.agent}",
            f"User: {user.display_name if user else 'unknown'}",
            f"Channel: {channel.display_name}",
            f"Context: {context}",
            f"Query: {text}",
            "Relevant docs:",
        ]
        for doc in docs:
            prompt_parts.append(f"- {doc['title']}: {doc['content'][:120]}")
        prompt = "\n".join(prompt_parts)
        llm = get_llm(self.agent)
        llm_result = llm.generate(prompt)
        tool_runs: list[dict[str, Any]] = []

        if self.agent == "accountant" and "reconcile" in text.lower():
            tool_result = tools.tool_reconcile(db, "INV-001")
            tool_runs.append({"tool": "reconcile", "result": tool_result})
        elif self.agent == "support" and "draft" in text.lower():
            tool_result = tools.tool_draft_email(
                to="maria@example.com",
                subject="Ticket update",
                body="We have prioritized your ticket and will reply shortly.",
            )
            tool_runs.append({"tool": "draft_email", "result": tool_result})
        elif self.agent == "copywriter" and "A/B".lower() in text.lower():
            tool_result = tools.tool_abtest_variants(
                db,
                page_id="landing",
                variants=[
                    {"key": "A", "text": "Variant A"},
                    {"key": "B", "text": "Variant B"},
                ],
            )
            tool_runs.append({"tool": "abtest", "result": tool_result})
        elif self.agent == "marketing" and "pause" in text.lower():
            tool_result = tools.tool_pause_ad("facebook", "f-1")
            tool_runs.append({"tool": "pause_ad", "result": tool_result})

        memory_utils.store_message(db, agent=self.agent, channel=channel, user=user, role="user", text=text)
        memory_utils.store_message(
            db,
            agent=self.agent,
            channel=channel,
            user=None,
            role="agent",
            text=llm_result.text,
        )
        if tool_runs:
            memory_utils.store_memory(
                db,
                agent=self.agent,
                channel=channel,
                user=user,
                kind="short_term",
                content=f"Tools used: {[run['tool'] for run in tool_runs]}",
            )
            memory_utils.store_memory(
                db,
                agent=self.agent,
                channel=channel,
                user=user,
                kind="tool_run",
                content=json.dumps(tool_runs, default=str),
            )
        if citations:
            memory_utils.store_memory(
                db,
                agent=self.agent,
                channel=channel,
                user=user,
                kind="citation",
                content=json.dumps(citations, default=str),
            )
        memory_utils.store_memory(
            db,
            agent=self.agent,
            channel=channel,
            user=user,
            kind="run_summary",
            content=json.dumps(
                {
                    "user_text": text,
                    "reply": llm_result.text,
                    "tool_runs": tool_runs,
                    "citations": citations,
                },
                default=str,
            ),
        )
        return AgentRunResult(reply=llm_result.text, tool_runs=tool_runs, citations=citations)


_GRAPHS = {
    "accountant": AgentGraph("accountant"),
    "support": AgentGraph("support"),
    "copywriter": AgentGraph("copywriter"),
    "marketing": AgentGraph("marketing"),
}


def build_agent_graph(agent_kind: str) -> AgentGraph:
    try:
        return _GRAPHS[agent_kind]
    except KeyError as exc:
        raise ValueError(f"Unknown agent: {agent_kind}") from exc


__all__ = ["AgentRunResult", "AgentGraph", "build_agent_graph"]
