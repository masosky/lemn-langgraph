"""Mock advertising adapters."""
from __future__ import annotations

from typing import Any


MOCK_REPORT = {
    "google": [
        {"ad_id": "g-1", "campaign": "Search", "spend": 300.0, "cpa": 45.0, "status": "active"},
        {"ad_id": "g-2", "campaign": "Brand", "spend": 150.0, "cpa": 20.0, "status": "active"},
    ],
    "facebook": [
        {"ad_id": "f-1", "campaign": "Retargeting", "spend": 200.0, "cpa": 55.0, "status": "active"},
    ],
}


def get_ads_report(platform: str, date_range: str) -> list[dict[str, Any]]:
    return MOCK_REPORT.get(platform.lower(), [])


def pause_ad(platform: str, ad_id: str) -> dict[str, Any]:
    ads = MOCK_REPORT.get(platform.lower(), [])
    for ad in ads:
        if ad["ad_id"] == ad_id:
            ad["status"] = "paused"
            return {"ok": True, "ad": ad}
    return {"ok": False, "error": "ad_not_found"}


__all__ = ["get_ads_report", "pause_ad", "MOCK_REPORT"]
