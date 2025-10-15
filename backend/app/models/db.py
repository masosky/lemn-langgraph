"""Database models and session utilities."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_ref: Mapped[str] = mapped_column(String, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String)

    messages: Mapped[list["Message"]] = relationship(back_populates="user")
    memories: Mapped[list["Memory"]] = relationship(back_populates="user")


class Channel(Base, TimestampMixin):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_ref: Mapped[str] = mapped_column(String, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String)
    platform: Mapped[str] = mapped_column(String, default="web")

    messages: Mapped[list["Message"]] = relationship(back_populates="channel")
    memories: Mapped[list["Memory"]] = relationship(back_populates="channel")


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent: Mapped[str] = mapped_column(String)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    role: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)

    channel: Mapped[Channel] = relationship(back_populates="messages")
    user: Mapped[User | None] = relationship(back_populates="messages")


class AgentRun(Base, TimestampMixin):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent: Mapped[str] = mapped_column(String, index=True)
    channel_id: Mapped[int | None] = mapped_column(ForeignKey("channels.id"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending", index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    input_text: Mapped[str] = mapped_column(Text)
    reply_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_runs_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    citations_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    channel: Mapped[Channel | None] = relationship()
    user: Mapped[User | None] = relationship()


class Memory(Base, TimestampMixin):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent: Mapped[str] = mapped_column(String)
    channel_id: Mapped[int | None] = mapped_column(ForeignKey("channels.id"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    kind: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)

    channel: Mapped[Channel | None] = relationship(back_populates="memories")
    user: Mapped[User | None] = relationship(back_populates="memories")


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    tags: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)


class ABTest(Base, TimestampMixin):
    __tablename__ = "abtests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    page_id: Mapped[str] = mapped_column(String)
    variant_key: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String, unique=True)
    customer: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)


class Ad(Base, TimestampMixin):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    platform: Mapped[str] = mapped_column(String)
    campaign: Mapped[str] = mapped_column(String)
    ad_id: Mapped[str] = mapped_column(String)
    spend: Mapped[float] = mapped_column(Float)
    cpa: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    priority: Mapped[str] = mapped_column(String)
    customer_email: Mapped[str] = mapped_column(String)


__all__ = [
    "Base",
    "User",
    "Channel",
    "Message",
    "AgentRun",
    "Memory",
    "Document",
    "ABTest",
    "Invoice",
    "Ad",
    "Ticket",
]
