"""Mock payment provider adapter (Stripe-like)."""
from __future__ import annotations

from typing import Any


def list_recent_payments() -> list[dict[str, Any]]:
    return [
        {"id": "pay_001", "amount": 120.0, "currency": "EUR", "status": "succeeded"},
        {"id": "pay_002", "amount": 89.0, "currency": "EUR", "status": "pending"},
    ]


__all__ = ["list_recent_payments"]
