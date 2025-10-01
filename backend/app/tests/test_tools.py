from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..graph import tools
from ..models.db import Base, Document
from ..services.abtest import record_variants


def setup_db():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, class_=Session, expire_on_commit=False)()


def test_vector_search_returns_results():
    db = setup_db()
    db.add_all([
        Document(title="One", tags="t", content="Hello world"),
        Document(title="Two", tags="t", content="Goodbye world"),
    ])
    db.commit()

    results = tools.vector_search(db, "hello", k=1)
    assert results
    assert results[0]["title"] == "One"


def test_abtest_records_variants():
    db = setup_db()
    variants = [{"key": "A", "text": "Variant A"}, {"key": "B", "text": "Variant B"}]
    stored = tools.tool_abtest_variants(db, "landing", variants)
    assert len(stored) == 2
    assert stored[0]["variant"] == "A"
