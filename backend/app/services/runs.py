from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal

from sqlalchemy.orm import Session

from ..models.db import AgentRun

RunStatus = Literal["pending", "completed", "interrupted", "failed"]
MultitaskStrategy = Literal["none", "interrupt"]


def _serialize(data: Any) -> str | None:
    if data is None:
        return None
    return json.dumps(data, default=str)


def interrupt_pending_run(
    db: Session,
    *,
    agent: str,
    channel_id: int | None,
    user_id: int | None,
) -> AgentRun | None:
    query = db.query(AgentRun).filter(AgentRun.agent == agent, AgentRun.status == "pending")
    if channel_id is not None:
        query = query.filter(AgentRun.channel_id == channel_id)
    if user_id is not None:
        query = query.filter(AgentRun.user_id == user_id)
    run = query.order_by(AgentRun.created_at.desc()).first()
    if run is None:
        return None
    run.status = "interrupted"
    run.completed_at = datetime.utcnow()
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def start_run(
    db: Session,
    *,
    agent: str,
    channel_id: int | None,
    user_id: int | None,
    input_text: str,
) -> AgentRun:
    run = AgentRun(
        agent=agent,
        channel_id=channel_id,
        user_id=user_id,
        status="pending",
        started_at=datetime.utcnow(),
        input_text=input_text,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def complete_run(
    db: Session,
    run_id: int,
    *,
    reply_text: str,
    tool_runs: list[dict[str, Any]] | None = None,
    citations: list[dict[str, Any]] | None = None,
) -> AgentRun:
    run = db.query(AgentRun).filter(AgentRun.id == run_id).one()
    run.status = "completed"
    run.completed_at = datetime.utcnow()
    run.reply_text = reply_text
    run.tool_runs_json = _serialize(tool_runs)
    run.citations_json = _serialize(citations)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def fail_run(db: Session, run_id: int, *, error_message: str) -> AgentRun:
    run = db.query(AgentRun).filter(AgentRun.id == run_id).one()
    run.status = "failed"
    run.completed_at = datetime.utcnow()
    run.error_message = error_message
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def serialize_run(run: AgentRun) -> dict[str, Any]:
    tool_runs = json.loads(run.tool_runs_json) if run.tool_runs_json else []
    citations = json.loads(run.citations_json) if run.citations_json else []
    return {
        "id": run.id,
        "status": run.status,
        "agent": run.agent,
        "channel_id": run.channel_id,
        "user_id": run.user_id,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "input_text": run.input_text,
        "reply_text": run.reply_text,
        "tool_runs": tool_runs,
        "citations": citations,
        "error_message": run.error_message,
    }
