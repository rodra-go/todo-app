from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Sequence

from .models import Priority, Status, TodoItem
from .repositories import TodoRepository


def create_todo(
    repo: TodoRepository,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[date] = None,
    priority: Optional[Priority] = None,
    tags: Optional[Sequence[str]] = None,
) -> TodoItem:
    """Create and persist a new TODO item.

    Args:
        repo: Repository used to persist the TODO item.
        title: Title of the TODO item.
        description: Optional description for the TODO item.
        due_date: Optional due date of the TODO item.
        priority: Optional priority for the TODO item.
        tags: Optional sequence of tags to associate with the TODO.

    Returns:
        The persisted TODO item with an assigned identifier.
    """
    now: datetime = datetime.utcnow()
    item_tags = [t.strip() for t in (tags or []) if t.strip()]
    item = TodoItem(
        id=None,
        title=title.strip(),
        description=description.strip() if description else None,
        status=Status.PENDING,
        created_at=now,
        updated_at=now,
        due_date=due_date,
        priority=priority,
        tags=item_tags,
    )
    return repo.add(item)


def list_todos(
    repo: TodoRepository,
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    due_today_or_overdue: bool = False,
    reference_date: Optional[date] = None,
) -> Sequence[TodoItem]:
    """List TODO items with optional filtering.

    Args:
        repo: Repository used to read TODO items.
        status: Optional status to filter by.
        priority: Optional priority to filter by.
        due_today_or_overdue: If True, restrict to TODOs with a due date that is
            on or before the reference_date.
        reference_date: Date used for due-date comparison. If None, today's date
            will be used when due_today_or_overdue is True.

    Returns:
        A sequence of TODO items after applying the filters.
    """
    items = list(repo.list_all())

    if status is not None:
        items = [item for item in items if item.status == status]

    if priority is not None:
        items = [item for item in items if item.priority == priority]

    if due_today_or_overdue:
        ref_date = reference_date or date.today()
        items = [
            item
            for item in items
            if item.due_date is not None and item.due_date <= ref_date
        ]

    return items


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


def update_todo(
    repo: TodoRepository,
    item_id: int,
    title: str,
    description: Optional[str],
    due_date: Optional[date],
    priority: Optional[Priority],
    tags: Optional[Sequence[str]],
) -> Optional[TodoItem]:
    """Update an existing TODO item.

    Args:
        repo: Repository used to persist changes.
        item_id: Identifier of the TODO item to update.
        title: New title for the TODO item.
        description: New description or None to clear it.
        due_date: New due date or None to clear it.
        priority: New priority or None to clear it.
        tags: New tags sequence or None to clear tags.

    Returns:
        The updated TODO item, or None if the item does not exist.
    """
    existing = repo.get(item_id)
    if existing is None:
        return None

    existing.title = title.strip()
    existing.description = description.strip() if description else None
    existing.due_date = due_date
    existing.priority = priority
    existing.tags = [t.strip() for t in (tags or []) if t.strip()]
    existing.updated_at = datetime.utcnow()
    return repo.update(existing)
