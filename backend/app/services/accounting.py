"""Mock accounting adapter for invoices."""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from ..models.db import Invoice


def fetch_invoices(db: Session, company_id: str | None = None) -> list[Invoice]:
    return db.query(Invoice).all()


def reconcile_invoice(db: Session, invoice_number: str) -> dict[str, Any]:
    invoice = db.query(Invoice).filter(Invoice.number == invoice_number).first()
    if not invoice:
        return {"ok": False, "error": "invoice_not_found"}
    invoice.status = "reconciled"
    db.add(invoice)
    db.commit()
    return {"ok": True, "invoice": invoice.number, "status": invoice.status}


__all__ = ["fetch_invoices", "reconcile_invoice"]
