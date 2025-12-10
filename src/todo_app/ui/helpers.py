from __future__ import annotations

from todo_app.domain.models import Priority


def priority_label_to_enum(label: str) -> Priority | None:
    """Convert a human-friendly priority label to a Priority enum."""
    mapping = {
        "Low": Priority.LOW,
        "Medium": Priority.MEDIUM,
        "High": Priority.HIGH,
    }
    return mapping.get(label)


def priority_enum_to_label(priority: Priority | None) -> str:
    """Convert a Priority enum to a readable UI label."""
    if priority is None:
        return "None"
    return priority.name.capitalize()


def parse_tags(raw: str) -> list[str]:
    """Convert comma-separated tag text into a clean list."""
    return [t.strip() for t in raw.split(",") if t.strip()]
