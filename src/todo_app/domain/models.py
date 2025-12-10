from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum, auto


class Status(Enum):
    """Status of a TODO item."""

    PENDING = auto()
    DONE = auto()


class Priority(Enum):
    """Priority level of a TODO item."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


@dataclass(slots=True)
class TodoItem:
    """Domain entity representing a TODO item.

    Attributes:
        id: Unique identifier in the persistence layer. None if not yet persisted.
        title: Short title of the TODO item.
        description: Optional longer description or notes.
        status: Current status of the TODO item.
        created_at: Timestamp when the item was created.
        updated_at: Timestamp when the item was last updated.
        due_date: Optional calendar date by which the TODO should be completed.
        priority: Optional priority level for the TODO item.
        tags: Optional list of free-form tags associated with the TODO.
    """

    id: int | None
    title: str
    description: str | None
    status: Status
    created_at: datetime
    updated_at: datetime
    due_date: date | None = None
    priority: Priority | None = None
    tags: list[str] = field(default_factory=list)
