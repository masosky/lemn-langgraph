"""Chat API endpoint."""
from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..agents import registry
from ..deps import get_db

router = APIRouter(prefix="/api")


class ChatRequest(BaseModel):
    agent: str
    channel_id: str = Field(default="default-web")
    user_id: str = Field(default="demo-user")
    text: str


class ToolRun(BaseModel):
    tool: str
    result: dict


class ChatResponse(BaseModel):
    reply: str
    tool_runs: list[ToolRun]
    citations: list[dict]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        agent_ctx = registry.get_agent(request.agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    result = agent_ctx.run(
        db,
        text=request.text,
        channel_ref=request.channel_id,
        user_ref=request.user_id,
    )

    return ChatResponse(
        reply=result.reply,
        tool_runs=[ToolRun(tool=run["tool"], result=run["result"]) for run in result.tool_runs],
        citations=result.citations,
    )
