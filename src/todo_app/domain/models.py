from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional


class Status(Enum):
    """Status of a TODO item."""

    PENDING = auto()
    DONE = auto()


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
    """

    id: Optional[int]
    title: str
    description: Optional[str]
    status: Status
    created_at: datetime
    updated_at: datetime
