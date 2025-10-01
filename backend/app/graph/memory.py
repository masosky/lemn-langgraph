"""Hybrid memory management utilities."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from ..models.db import Channel, Document, Memory, Message, User

SHORT_TERM_WINDOW = 5


def get_or_create_user(db: Session, external_ref: str, display_name: str) -> User:
    user = db.query(User).filter(User.external_ref == external_ref).first()
    if not user:
        user = User(external_ref=external_ref, display_name=display_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user(db: Session, external_ref: str) -> User | None:
    """Return an existing user without creating a new row."""

    return db.query(User).filter(User.external_ref == external_ref).first()


def get_or_create_channel(db: Session, external_ref: str, display_name: str, platform: str) -> Channel:
    channel = db.query(Channel).filter(Channel.external_ref == external_ref).first()
    if not channel:
        channel = Channel(external_ref=external_ref, display_name=display_name, platform=platform)
        db.add(channel)
        db.commit()
        db.refresh(channel)
    return channel


def store_message(
    db: Session,
    *,
    agent: str,
    channel: Channel,
    user: User | None,
    role: str,
    text: str,
) -> Message:
    message = Message(agent=agent, channel_id=channel.id, user_id=user.id if user else None, role=role, text=text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def store_memory(
    db: Session,
    *,
    agent: str,
    channel: Channel | None,
    user: User | None,
    kind: str,
    content: str,
) -> Memory:
    memory = Memory(
        agent=agent,
        channel_id=channel.id if channel else None,
        user_id=user.id if user else None,
        kind=kind,
        content=content,
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


def fetch_recent_messages(db: Session, agent: str, channel_id: int, user_id: int | None) -> list[Message]:
    query = db.query(Message).filter(Message.agent == agent, Message.channel_id == channel_id)
    if user_id:
        query = query.filter(Message.user_id == user_id)
    return query.order_by(Message.created_at.desc()).limit(SHORT_TERM_WINDOW).all()


def fetch_memories(
    db: Session,
    agent: str,
    channel_id: int | None,
    *,
    user_id: int | None = None,
    limit: int = 10,
) -> list[Memory]:
    """Return recent memories filtered by channel and optionally user."""

    query = db.query(Memory).filter(Memory.agent == agent)
    if channel_id is not None:
        query = query.filter(Memory.channel_id == channel_id)
    if user_id is not None:
        query = query.filter(Memory.user_id == user_id)
    return query.order_by(Memory.created_at.desc()).limit(limit).all()


def fetch_agent_documents(db: Session, agent: str, limit: int = 5) -> list[Document]:
    """Return documents tagged for a given agent, falling back to recent docs."""

    tag = agent.lower()
    query = db.query(Document)
    tagged_docs = (
        query.filter(Document.tags.ilike(f"%{tag}%"))
        .order_by(Document.created_at.desc())
        .limit(limit)
        .all()
    )
    if len(tagged_docs) >= limit:
        return tagged_docs
    remaining = limit - len(tagged_docs)
    if remaining <= 0:
        return tagged_docs
    fallback_docs = (
        query.filter(~Document.tags.ilike(f"%{tag}%"))
        .order_by(Document.created_at.desc())
        .limit(remaining)
        .all()
    )
    return tagged_docs + fallback_docs


__all__ = [
    "get_or_create_user",
    "get_or_create_channel",
    "store_message",
    "store_memory",
    "fetch_recent_messages",
    "get_user",
    "fetch_memories",
    "fetch_agent_documents",
]
