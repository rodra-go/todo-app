from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from .models import TodoItem, Status, Priority


def apply_filters(
    items: Iterable[TodoItem],
    status: Optional[Status] = None,
    text_query: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[TodoItem]:
    """Filter items in memory."""

def sort_items(
    items: Sequence[TodoItem],
    by_due_date: bool = False,
    by_priority: bool = False,
) -> List[TodoItem]:
    """Sort items in memory."""
