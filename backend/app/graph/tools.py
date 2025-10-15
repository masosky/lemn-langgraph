"""Tool implementations used by agents."""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from ..models.db import Document, Memory
from ..services import accounting, ads, mail, slack as slack_service
from ..services.embeddings import FakeEmbeddingProvider, cosine_similarity
from ..services.abtest import record_variants


_embedder = FakeEmbeddingProvider()
_slack_client = slack_service.SlackClient()


def vector_search(db: Session, query: str, k: int = 4) -> list[dict[str, Any]]:
    query_vector = _embedder.embed(query)
    documents = db.query(Document).all()
    scored: list[tuple[float, Document]] = []
    for doc in documents:
        doc_vector = _embedder.embed(doc.content)
        score = cosine_similarity(query_vector, doc_vector)
        scored.append((score, doc))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    results = []
    for score, doc in scored[:k]:
        results.append({"title": doc.title, "score": score, "content": doc.content})
    return results


def tool_post_to_slack(channel: str, text: str) -> dict[str, Any]:
    return _slack_client.post_message(channel, text)


def tool_fetch_invoices(db: Session, company_id: str | None = None) -> list[dict[str, Any]]:
    invoices = accounting.fetch_invoices(db, company_id)
    return [
        {
            "number": invoice.number,
            "customer": invoice.customer,
            "amount": invoice.amount,
            "status": invoice.status,
        }
        for invoice in invoices
    ]


def tool_reconcile(db: Session, invoice_number: str) -> dict[str, Any]:
    return accounting.reconcile_invoice(db, invoice_number)


def tool_fetch_tickets(db: Session, status: str | None = None) -> list[dict[str, Any]]:
    from ..models.db import Ticket

    query = db.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    return [
        {
            "id": ticket.id,
            "subject": ticket.subject,
            "status": ticket.status,
            "priority": ticket.priority,
            "customer_email": ticket.customer_email,
        }
        for ticket in query.all()
    ]


def tool_draft_email(to: str, subject: str, body: str) -> dict[str, Any]:
    return mail.draft_email(to, subject, body)


def tool_translate(text: str, target_lang: str) -> dict[str, str]:
    return {"text": f"[{target_lang.upper()}] {text}"}


def tool_abtest_variants(db: Session, page_id: str, variants: list[dict[str, str]]) -> list[dict[str, Any]]:
    records = record_variants(db, page_id, variants)
    return [
        {
            "variant": record.variant_key,
            "impressions": record.impressions,
            "conversions": record.conversions,
        }
        for record in records
    ]


def tool_get_ads_report(platform: str, date_range: str) -> list[dict[str, Any]]:
    return ads.get_ads_report(platform, date_range)


def tool_pause_ad(platform: str, ad_id: str) -> dict[str, Any]:
    return ads.pause_ad(platform, ad_id)


__all__ = [
    "vector_search",
    "tool_post_to_slack",
    "tool_fetch_invoices",
    "tool_reconcile",
    "tool_fetch_tickets",
    "tool_draft_email",
    "tool_translate",
    "tool_abtest_variants",
    "tool_get_ads_report",
    "tool_pause_ad",
]
