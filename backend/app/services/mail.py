"""Mock Gmail adapter."""
from __future__ import annotations

from typing import Any


def draft_email(to: str, subject: str, body: str) -> dict[str, Any]:
    return {
        "ok": True,
        "to": to,
        "subject": subject,
        "body": body,
        "preview": body[:120],
    }


__all__ = ["draft_email"]
