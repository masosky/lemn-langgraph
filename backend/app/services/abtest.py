"""Simple A/B testing harness."""
from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.db import ABTest


def record_variants(db: Session, page_id: str, variants: list[dict[str, str]]) -> list[ABTest]:
    records: list[ABTest] = []
    for idx, variant in enumerate(variants, start=1):
        record = ABTest(
            page_id=page_id,
            variant_key=variant.get("key", f"variant_{idx}"),
            text=variant.get("text", ""),
            impressions=variant.get("impressions", 100 + idx * 10),
            conversions=variant.get("conversions", 10 + idx * 2),
        )
        db.add(record)
        records.append(record)
    db.commit()
    return records


__all__ = ["record_variants"]
