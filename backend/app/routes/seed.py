"""Seed endpoint to populate demo data."""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.db import ABTest, Ad, Document, Invoice, Ticket

router = APIRouter()


@router.post("/seed")
def seed(db: Session = Depends(get_db)) -> dict[str, int]:
    documents = [
        Document(title="Brand Voice", tags="copywriter", content="We speak with clarity and optimism."),
        Document(title="Accounting Policy", tags="accountant", content="Always reconcile invoices within 7 days."),
        Document(title="Support Playbook", tags="support", content="Respond with empathy and provide clear next steps."),
        Document(title="Marketing Guardrails", tags="marketing", content="Avoid overpromising results and respect privacy."),
    ]
    invoices = [
        Invoice(number="INV-001", customer="Acme Corp", amount=1200.0, status="pending"),
        Invoice(number="INV-002", customer="Globex", amount=850.0, status="pending"),
    ]
    ads = [
        Ad(platform="facebook", campaign="Retargeting", ad_id="f-1", spend=200.0, cpa=55.0, status="active"),
        Ad(platform="google", campaign="Search", ad_id="g-1", spend=300.0, cpa=45.0, status="active"),
    ]
    tickets = [
        Ticket(subject="Issue with billing", status="open", priority="high", customer_email="maria@example.com"),
        Ticket(subject="Login problem", status="open", priority="medium", customer_email="lee@example.com"),
    ]

    for collection in (documents, invoices, ads, tickets):
        for item in collection:
            db.merge(item)
    db.commit()
    return {
        "documents": len(documents),
        "invoices": len(invoices),
        "ads": len(ads),
        "tickets": len(tickets),
    }
