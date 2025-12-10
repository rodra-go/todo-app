from __future__ import annotations

from abc import abstractmethod
from typing import Optional, Protocol, Sequence

from .models import Status, TodoItem


class TodoRepository(Protocol):
    """Abstraction for persisting and retrieving TODO items."""

    @abstractmethod
    def add(self, item: TodoItem) -> TodoItem:
        """Persist a new TODO item and return it with an assigned id."""

    @abstractmethod
    def list_all(self) -> Sequence[TodoItem]:
        """Return all TODO items."""

    @abstractmethod
    def get(self, item_id: int) -> Optional[TodoItem]:
        """Retrieve a TODO item by its id."""

    @abstractmethod
    def update(self, item: TodoItem) -> TodoItem:
        """Update an existing TODO item and return the updated entity."""

    @abstractmethod
    def delete(self, item_id: int) -> None:
        """Delete a TODO item by its id."""

    @abstractmethod
    def set_status(self, item_id: int, status: Status) -> Optional[TodoItem]:
        """Set the status of a TODO item and return the updated item, or None if not found."""
