"""Common FastAPI dependencies."""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_settings
from .models.db import Base

_engine = None
_SessionLocal: sessionmaker | None = None


def _get_engine():
    global _engine, _SessionLocal
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings.database_url, future=True)
        _SessionLocal = sessionmaker(bind=_engine, class_=Session, expire_on_commit=False)
        Base.metadata.create_all(bind=_engine)
    return _engine


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session and close it afterwards."""

    if _SessionLocal is None:
        _get_engine()
    assert _SessionLocal is not None
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
