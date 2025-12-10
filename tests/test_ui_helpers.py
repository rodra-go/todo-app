from __future__ import annotations

from todo_app.domain.models import Priority
from todo_app.ui.helpers import (
    parse_tags,
    priority_enum_to_label,
    priority_label_to_enum,
)


class TestPriorityLabelToEnum:
    def test_known_labels_are_mapped(self) -> None:
        assert priority_label_to_enum("Low") == Priority.LOW
        assert priority_label_to_enum("Medium") == Priority.MEDIUM
        assert priority_label_to_enum("High") == Priority.HIGH

    def test_unknown_label_returns_none(self) -> None:
        assert priority_label_to_enum("Unknown") is None
        assert priority_label_to_enum("") is None


class TestPriorityEnumToLabel:
    def test_none_priority_returns_none_label(self) -> None:
        assert priority_enum_to_label(None) == "None"

    def test_priority_values_are_capitalized(self) -> None:
        assert priority_enum_to_label(Priority.LOW) == "Low"
        assert priority_enum_to_label(Priority.MEDIUM) == "Medium"
        assert priority_enum_to_label(Priority.HIGH) == "High"


class TestParseTags:
    def test_parses_comma_separated_tags(self) -> None:
        raw = "work, personal, errands"
        assert parse_tags(raw) == ["work", "personal", "errands"]

    def test_trims_whitespace_and_ignores_empty(self) -> None:
        raw = "  work , , personal ,  ,  errands  "
        assert parse_tags(raw) == ["work", "personal", "errands"]

    def test_empty_string_returns_empty_list(self) -> None:
        assert parse_tags("") == []

    def test_only_commas_and_spaces_returns_empty_list(self) -> None:
        assert parse_tags(" , ,  , ") == []
