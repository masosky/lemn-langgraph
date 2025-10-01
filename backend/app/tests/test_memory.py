from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..graph import memory
from ..models.db import Base, Document


def setup_db():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, class_=Session, expire_on_commit=False)()


def test_store_and_fetch_memory():
    db = setup_db()
    user = memory.get_or_create_user(db, "user-1", "User One")
    channel = memory.get_or_create_channel(db, "chan-1", "Channel One", "web")
    memory.store_message(db, agent="support", channel=channel, user=user, role="user", text="Hello")
    memory.store_memory(db, agent="support", channel=channel, user=user, kind="short_term", content="note")

    messages = memory.fetch_recent_messages(db, "support", channel.id, user.id)
    assert len(messages) == 1
    assert messages[0].text == "Hello"

    memories = memory.fetch_memories(db, "support", channel.id)
    assert len(memories) == 1
    assert memories[0].content == "note"


def test_fetch_memories_with_user_filter():
    db = setup_db()
    alice = memory.get_or_create_user(db, "alice", "Alice")
    bob = memory.get_or_create_user(db, "bob", "Bob")
    channel = memory.get_or_create_channel(db, "chan-1", "Channel One", "web")
    memory.store_memory(db, agent="support", channel=channel, user=alice, kind="short_term", content="alice-note")
    memory.store_memory(db, agent="support", channel=channel, user=bob, kind="short_term", content="bob-note")

    alice_memories = memory.fetch_memories(db, "support", channel.id, user_id=alice.id)
    assert len(alice_memories) == 1
    assert alice_memories[0].content == "alice-note"

    all_memories = memory.fetch_memories(db, "support", channel.id)
    assert len(all_memories) == 2


def test_fetch_agent_documents_prefers_tag_matches():
    db = setup_db()
    doc_general = Document(title="General", tags="shared", content="General guidance")
    doc_support = Document(title="Support KB", tags="support", content="Support specific guidance")
    doc_support_extra = Document(title="Support KB 2", tags="support", content="More support help")
    db.add_all([doc_general, doc_support, doc_support_extra])
    db.commit()

    docs = memory.fetch_agent_documents(db, "support", limit=2)
    assert [doc.title for doc in docs] == ["Support KB", "Support KB 2"]

    marketing_docs = memory.fetch_agent_documents(db, "marketing", limit=2)
    assert len(marketing_docs) == 2
    assert marketing_docs[0].title in {"General", "Support KB", "Support KB 2"}
