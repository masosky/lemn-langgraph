from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.db import Memory, Message

router = APIRouter(prefix="/api")

AGENT_METADATA = [
    {"id": "accountant", "title": "Accountant", "description": "Finance reconciliation"},
    {"id": "support", "title": "Support", "description": "Customer support"},
    {"id": "copywriter", "title": "Copywriter", "description": "Marketing copy"},
    {"id": "marketing", "title": "Marketing Analyst", "description": "Campaign insights"},
]


@router.get("/overview")
def overview(db: Session = Depends(get_db)) -> dict[str, Any]:
    total_messages = db.query(func.count(Message.id)).scalar() or 0
    total_memories = db.query(func.count(Memory.id)).scalar() or 0
    agent_stats: list[dict[str, Any]] = []
    active_agents = 0
    for meta in AGENT_METADATA:
        message_count = db.query(func.count(Message.id)).filter(Message.agent == meta["id"]).scalar() or 0
        conversation_count = (
            db.query(func.count(func.distinct(Message.channel_id))).filter(Message.agent == meta["id"]).scalar() or 0
        )
        last_interaction = (
            db.query(func.max(Message.created_at)).filter(Message.agent == meta["id"]).scalar()
        )
        tool_runs = (
            db.query(func.count(Memory.id))
            .filter(Memory.agent == meta["id"], Memory.kind == "tool_run")
            .scalar()
            or 0
        )
        if message_count:
            active_agents += 1
        agent_stats.append(
            {
                "id": meta["id"],
                "title": meta["title"],
                "description": meta["description"],
                "messages": message_count,
                "conversations": conversation_count,
                "tool_runs": tool_runs,
                "last_interaction": last_interaction.isoformat() if last_interaction else None,
            }
        )
    return {
        "total_messages": total_messages,
        "total_memories": total_memories,
        "active_agents": active_agents,
        "agent_stats": agent_stats,
    }


@router.get("/runs/{agent}")
def runs(
    agent: str,
    db: Session = Depends(get_db),
    limit: int = Query(default=5, ge=1, le=20),
) -> dict[str, Any]:
    if agent not in {meta["id"] for meta in AGENT_METADATA}:
        raise HTTPException(status_code=404, detail="Unknown agent")
    query = (
        db.query(Memory)
        .filter(Memory.agent == agent, Memory.kind == "run_summary")
        .order_by(Memory.created_at.desc())
        .limit(limit)
    )
    rows = query.all()
    runs_payload: list[dict[str, Any]] = []
    for memory in rows:
        try:
            payload = json.loads(memory.content)
        except json.JSONDecodeError:
            payload = {}
        runs_payload.append(
            {
                "id": memory.id,
                "created_at": memory.created_at.isoformat(),
                "channel": memory.channel.external_ref if memory.channel else None,
                "user": memory.user.external_ref if memory.user else None,
                "user_text": payload.get("user_text", ""),
                "reply": payload.get("reply", ""),
                "tool_runs": payload.get("tool_runs", []),
                "citations": payload.get("citations", []),
            }
        )
    return {"agent": agent, "runs": runs_payload}
