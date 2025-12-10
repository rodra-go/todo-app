from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import List, Optional, Sequence

from todo_app.domain.models import Priority, Status, TodoItem
from todo_app.domain.repositories import TodoRepository
from todo_app.domain.services import (
    create_todo,
    list_todos,
    toggle_done,
)


class InMemoryTodoRepository(TodoRepository):
    """Simple in-memory repository for testing domain services."""

    def __init__(self) -> None:
        """Initialize an empty in-memory store."""
        self._items: List[TodoItem] = []
        self._next_id: int = 1

    def add(self, item: TodoItem) -> TodoItem:
        item.id = self._next_id
        self._next_id += 1
        self._items.append(item)
        return item

    def list_all(self) -> Sequence[TodoItem]:
        return list(self._items)

    def get(self, item_id: int) -> Optional[TodoItem]:
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def update(self, item: TodoItem) -> TodoItem:
        for idx, existing in enumerate(self._items):
            if existing.id == item.id:
                self._items[idx] = item
                return item
        msg = f"Item with id {item.id} not found"
        raise ValueError(msg)

    def delete(self, item_id: int) -> None:
        self._items = [item for item in self._items if item.id != item_id]

    def set_status(self, item_id: int, status: Status) -> Optional[TodoItem]:
        item = self.get(item_id)
        if item is None:
            return None
        item.status = status
        item.updated_at = datetime.utcnow()
        return item


def test_create_and_list_todo() -> None:
    """Creating a TODO should store it and make it appear in the list."""
    repo = InMemoryTodoRepository()
    created = create_todo(
        repo=repo,
        title="Test",
        description="Example",
        priority=Priority.HIGH,
        tags=["work", "urgent"],
    )

    assert created.id is not None
    assert created.title == "Test"
    assert created.status == Status.PENDING
    assert created.priority == Priority.HIGH
    assert "work" in created.tags

    items = list_todos(repo=repo)
    assert len(items) == 1
    assert items[0].title == "Test"


def test_toggle_done_changes_status() -> None:
    """Toggling a TODO should switch between pending and done."""
    repo = InMemoryTodoRepository()
    created = create_todo(repo=repo, title="Test toggle")

    assert created.status == Status.PENDING

    updated = toggle_done(repo=repo, item_id=created.id or 0)
    assert updated is not None
    assert updated.status == Status.DONE

    updated_again = toggle_done(repo=repo, item_id=created.id or 0)
    assert updated_again is not None
    assert updated_again.status == Status.PENDING


def test_due_today_or_overdue_filter() -> None:
    """Filtering by due_today_or_overdue should respect the reference date."""
    repo = InMemoryTodoRepository()
    ref_date = date(2025, 1, 10)

    create_todo(
        repo=repo,
        title="Overdue",
        due_date=ref_date - timedelta(days=1),
    )
    create_todo(
        repo=repo,
        title="Due today",
        due_date=ref_date,
    )
    create_todo(
        repo=repo,
        title="Future",
        due_date=ref_date + timedelta(days=1),
    )
    create_todo(
        repo=repo,
        title="No due date",
        due_date=None,
    )

    filtered = list_todos(
        repo=repo,
        due_today_or_overdue=True,
        reference_date=ref_date,
    )
    titles = {item.title for item in filtered}
    assert "Overdue" in titles
    assert "Due today" in titles
    assert "Future" not in titles
    assert "No due date" not in titles
