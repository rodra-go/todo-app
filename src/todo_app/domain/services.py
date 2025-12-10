from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from .models import Status, TodoItem
from .repositories import TodoRepository


def create_todo(
    repo: TodoRepository,
    title: str,
    description: Optional[str] = None,
) -> TodoItem:
    """Create and persist a new TODO item.

    Args:
        repo: Repository used to persist the TODO item.
        title: Title of the TODO item.
        description: Optional description for the TODO item.

    Returns:
        The persisted TODO item with an assigned identifier.
    """
    now: datetime = datetime.utcnow()
    item = TodoItem(
        id=None,
        title=title.strip(),
        description=description.strip() if description else None,
        status=Status.PENDING,
        created_at=now,
        updated_at=now,
    )
    return repo.add(item)


def list_todos(repo: TodoRepository) -> Sequence[TodoItem]:
    """List all TODO items.

    Args:
        repo: Repository used to read TODO items.

    Returns:
        A sequence of all TODO items.
    """
    return repo.list_all()


def toggle_done(repo: TodoRepository, item_id: int) -> Optional[TodoItem]:
    """Toggle the status of a TODO item between pending and done.

    Args:
        repo: Repository used to update the TODO item.
        item_id: Identifier of the TODO item to toggle.

    Returns:
        The updated TODO item, or None if no item exists with the given id.
    """
    item = repo.get(item_id)
    if item is None:
        return None

    new_status = Status.DONE if item.status == Status.PENDING else Status.PENDING
    return repo.set_status(item_id=item_id, status=new_status)
