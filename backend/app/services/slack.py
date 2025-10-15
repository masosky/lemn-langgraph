"""Slack client wrapper supporting mock mode."""
from __future__ import annotations

import logging
from typing import Any

from ..config import get_settings

logger = logging.getLogger(__name__)


class SlackClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def post_message(self, channel: str, text: str, thread_ts: str | None = None) -> dict[str, Any]:
        if not self.settings.slack.enabled:
            logger.info("[SlackMock] channel=%s text=%s", channel, text)
            return {"ok": True, "channel": channel, "text": text, "mock": True}
        # In a real implementation we'd call Slack Web API. For the showcase we log.
        logger.info("[SlackReal] channel=%s text=%s", channel, text)
        return {"ok": True, "channel": channel, "text": text}


__all__ = ["SlackClient"]
