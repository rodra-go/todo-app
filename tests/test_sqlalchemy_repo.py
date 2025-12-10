from __future__ import annotations

from collections.abc import Iterator
from datetime import date, datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from todo_app.domain.models import Priority, Status, TodoItem
from todo_app.infrastructure.db import Base
from todo_app.infrastructure.repositories import SqlAlchemyTodoRepository


@pytest.fixture()
def engine(tmp_path: Path) -> Engine:
    """Create a temporary SQLite engine bound to a file per test."""
    db_path = tmp_path / "test_repo.db"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture()
def session_factory(engine: Engine) -> sessionmaker[Session]:
    """Return a session factory bound to the temporary engine."""
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=Session,
    )


@pytest.fixture()
def repo(session_factory: sessionmaker[Session]) -> Iterator[SqlAlchemyTodoRepository]:
    """Yield a repository backed by the temporary SQLite database."""
    yield SqlAlchemyTodoRepository(session_factory)


def _make_item(
    title: str = "Task",
    description: str | None = None,
    status: Status = Status.PENDING,
    priority: Priority | None = None,
) -> TodoItem:
    """Helper to create a TodoItem with timestamps set."""
    now = datetime.utcnow()
    return TodoItem(
        id=None,
        title=title,
        description=description,
        status=status,
        created_at=now,
        updated_at=now,
        due_date=date.today(),
        priority=priority,
        tags=["repo", "test"],
    )


def test_add_and_get_roundtrip(repo: SqlAlchemyTodoRepository) -> None:
    """Adding an item should roundtrip through the database correctly."""
    item = _make_item(
        title="DB task",
        description="stored in sqlite",
        priority=Priority.MEDIUM,
    )
    saved = repo.add(item)

    assert saved.id is not None
    assert saved.title == "DB task"
    assert saved.priority == Priority.MEDIUM
    assert "repo" in saved.tags

    fetched = repo.get(saved.id or 0)
    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.title == "DB task"
    assert fetched.priority == Priority.MEDIUM
    assert fetched.due_date == saved.due_date


def test_list_all_orders_by_created_at_desc(
    repo: SqlAlchemyTodoRepository,
) -> None:
    """list_all should return items ordered by created_at descending."""
    first = _make_item(title="first")
    second = _make_item(title="second")
    # Simulate different creation times by adjusting timestamps.
    second.created_at = first.created_at.replace(
        microsecond=first.created_at.microsecond + 1
    )

    repo.add(first)
    repo.add(second)

    items = list(repo.list_all())
    titles = [item.title for item in items]
    # Second is newer, so should come first.
    assert titles[0] == "second"
    assert titles[1] == "first"


def test_set_status_persists_status_change(
    repo: SqlAlchemyTodoRepository,
) -> None:
    """set_status should update the stored status in the database."""
    item = _make_item(title="status-change")
    saved = repo.add(item)

    updated = repo.set_status(saved.id or 0, Status.DONE)
    assert updated is not None
    assert updated.status == Status.DONE

    fetched = repo.get(saved.id or 0)
    assert fetched is not None
    assert fetched.status == Status.DONE
