"""Memory inspection endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..deps import get_db
from ..graph.memory import (
    fetch_agent_documents,
    fetch_memories,
    get_or_create_channel,
    get_user,
)

router = APIRouter()


@router.get("/memory/{agent}/{channel_id}")
def get_memory(
    agent: str,
    channel_id: str,
    db: Session = Depends(get_db),
    user_id: str | None = Query(default=None, description="Optional user external reference"),
    limit: int = Query(default=10, ge=1, le=50),
    documents: int = Query(default=4, ge=1, le=10),
) -> dict:
    channel = get_or_create_channel(db, channel_id, channel_id, "web")
    user = get_user(db, user_id) if user_id else None
    memories = fetch_memories(
        db,
        agent,
        channel.id,
        user_id=user.id if user else None,
        limit=limit,
    )
    doc_rows = fetch_agent_documents(db, agent, limit=documents)
    return {
        "agent": agent,
        "channel": channel.external_ref,
        "user": user.external_ref if user else None,
        "memories": [
            {"kind": memory.kind, "content": memory.content, "created_at": memory.created_at}
            for memory in memories
        ],
        "documents": [
            {
                "title": doc.title,
                "tags": doc.tags,
                "snippet": doc.content[:200],
                "created_at": doc.created_at,
            }
            for doc in doc_rows
        ],
    }
