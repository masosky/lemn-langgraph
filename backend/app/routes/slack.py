"""Slack events endpoint (mock-friendly)."""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from ..agents import registry
from ..config import get_settings
from ..deps import get_db
from ..services.slack import SlackClient

logger = logging.getLogger(__name__)

router = APIRouter()


def verify_signature(body: bytes, timestamp: str, signature: str) -> bool:
    settings = get_settings()
    if not settings.slack.signing_secret:
        return True
    basestring = f"v0:{timestamp}:{body.decode()}".encode()
    digest = hmac.new(settings.slack.signing_secret.encode(), basestring, hashlib.sha256).hexdigest()
    expected = f"v0={digest}"
    return hmac.compare_digest(expected, signature)


@router.post("/slack/events")
async def slack_events(
    request: Request,
    db: Session = Depends(get_db),
    x_slack_request_timestamp: str = Header(default="0"),
    x_slack_signature: str = Header(default=""),
) -> dict[str, Any]:
    raw_body = await request.body()
    if not verify_signature(raw_body, x_slack_request_timestamp, x_slack_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge", "")}

    event = payload.get("event", {})
    text = event.get("text", "")
    user_id = event.get("user", "slack-user")
    channel_id = event.get("channel", "slack-channel")

    agent_key = "support"
    lowered = text.lower()
    if "accountant" in lowered:
        agent_key = "accountant"
    elif "copywriter" in lowered:
        agent_key = "copywriter"
    elif "marketing" in lowered:
        agent_key = "marketing"

    agent_ctx = registry.get_agent(agent_key)
    result = agent_ctx.run(
        db,
        text=text,
        channel_ref=channel_id,
        user_ref=user_id,
        platform="slack",
    )
    SlackClient().post_message(channel_id, result.reply)
    return {"ok": True, "reply": result.reply}
