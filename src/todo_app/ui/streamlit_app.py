from __future__ import annotations

from datetime import date

import streamlit as st

from todo_app.domain.models import Priority, Status, TodoItem
from todo_app.domain.services import create_todo, list_todos, toggle_done, update_todo
from todo_app.infrastructure.db import get_session_factory, init_db
from todo_app.infrastructure.repositories import SqlAlchemyTodoRepository


def get_repo() -> SqlAlchemyTodoRepository:
    """Retrieve a singleton repository instance stored in Streamlit session state.

    Returns:
        A SqlAlchemyTodoRepository instance.
    """
    if "todo_repo" not in st.session_state:
        session_factory = get_session_factory()
        st.session_state["todo_repo"] = SqlAlchemyTodoRepository(session_factory)
    return st.session_state["todo_repo"]


def _priority_label_to_enum(label: str) -> Priority | None:
    """Convert a human-friendly priority label into a Priority enum.

    Args:
        label: Label selected in the UI.

    Returns:
        Priority enum instance or None if label represents 'All' or 'None'.
    """
    mapping: dict[str, Priority] = {
        "Low": Priority.LOW,
        "Medium": Priority.MEDIUM,
        "High": Priority.HIGH,
    }
    return mapping.get(label)


def _priority_enum_to_label(priority: Priority | None) -> str:
    """Convert a Priority enum to a UI label.

    Args:
        priority: Priority enum or None.

    Returns:
        Readable label used in UI controls.
    """
    if priority is None:
        return "None"
    if priority == Priority.LOW:
        return "Low"
    if priority == Priority.MEDIUM:
        return "Medium"
    return "High"


def _parse_tags(raw: str) -> list[str]:
    """Parse a comma-separated tag string into a list of tags.

    Args:
        raw: Raw string from the UI.

    Returns:
        List of cleaned tags.
    """
    return [t.strip() for t in raw.split(",") if t.strip()]


def render_create_form() -> None:
    """Render the form to create a new TODO item."""
    st.subheader("Add TODO")
    with st.form("create_todo_form", clear_on_submit=True):
        title: str = st.text_input("Title", "")
        description: str = st.text_area("Description", "")

        use_due_date: bool = st.checkbox("Set due date?", value=False)
        due_date_value: date | None = None
        if use_due_date:
            due_date_value = st.date_input("Due date", value=date.today())

        priority_label: str = st.selectbox(
            "Priority",
            options=["Medium", "Low", "High"],
            index=0,
        )
        priority = _priority_label_to_enum(priority_label)

        tags_raw: str = st.text_input("Tags (comma separated)", "")

        submitted = st.form_submit_button("Add")
        if submitted:
            if not title.strip():
                st.warning("Title is required.")
            else:
                repo = get_repo()
                create_todo(
                    repo=repo,
                    title=title,
                    description=description,
                    due_date=due_date_value,
                    priority=priority,
                    tags=_parse_tags(tags_raw),
                )
                st.success("TODO created.")


def render_filters() -> tuple[Status | None, Priority | None, bool]:
    """Render filter controls and return chosen filter values.

    Returns:
        Tuple of (status_filter, priority_filter, due_today_or_overdue).
    """
    st.subheader("Filters")
    cols = st.columns(3)

    with cols[0]:
        status_option = st.selectbox(
            "Status",
            options=["All", "Pending", "Done"],
            index=0,
        )
        status_filter: Status | None
        if status_option == "Pending":
            status_filter = Status.PENDING
        elif status_option == "Done":
            status_filter = Status.DONE
        else:
            status_filter = None

    with cols[1]:
        priority_option = st.selectbox(
            "Priority",
            options=["All", "Low", "Medium", "High"],
            index=0,
        )
        priority_filter: Priority | None
        if priority_option == "All":
            priority_filter = None
        else:
            priority_filter = _priority_label_to_enum(priority_option)

    with cols[2]:
        due_today_or_overdue = st.checkbox("Due today or overdue", value=False)

    return status_filter, priority_filter, due_today_or_overdue


def render_todo_list(
    status_filter: Status | None,
    priority_filter: Priority | None,
    due_today_or_overdue: bool,
) -> None:
    """Render the list of existing TODO items with toggle and edit actions.

    Args:
        status_filter: Optional status filter.
        priority_filter: Optional priority filter.
        due_today_or_overdue: Whether to restrict to items due today or overdue.
    """
    st.subheader("TODOs")

    repo = get_repo()
    items = list_todos(
        repo=repo,
        status=status_filter,
        priority=priority_filter,
        due_today_or_overdue=due_today_or_overdue,
    )

    if not items:
        st.info("No TODOs match the current filters.")
        return

    for item in items:
        _render_todo_row(item)


def _on_toggle(item_id: int) -> None:
    """Handle checkbox toggle for a TODO item.

    Args:
        item_id: Identifier of the TODO item to toggle.
    """
    repo = get_repo()
    toggle_done(repo=repo, item_id=item_id)


def _render_edit_form(item: TodoItem) -> None:
    """Render an inline edit form for a TODO item.

    Args:
        item: TODO item to edit.
    """
    with st.expander("Edit", expanded=False):
        with st.form(f"edit_form_{item.id}"):
            title: str = st.text_input("Title", value=item.title)
            description: str = st.text_area(
                "Description",
                value=item.description or "",
            )

            has_due = st.checkbox(
                "Set due date?",
                value=item.due_date is not None,
                key=f"edit_due_checkbox_{item.id}",
            )
            due_date_value: date | None = item.due_date
            if has_due:
                due_date_value = st.date_input(
                    "Due date",
                    value=item.due_date or date.today(),
                    key=f"edit_due_date_{item.id}",
                )
            else:
                due_date_value = None

            priority_label = st.selectbox(
                "Priority",
                options=["None", "Low", "Medium", "High"],
                index=[
                    "None",
                    "Low",
                    "Medium",
                    "High",
                ].index(_priority_enum_to_label(item.priority)),
                key=f"edit_priority_{item.id}",
            )
            priority: Priority | None
            if priority_label == "None":
                priority = None
            else:
                priority = _priority_label_to_enum(priority_label)

            tags_raw = st.text_input(
                "Tags (comma separated)",
                value=",".join(item.tags),
                key=f"edit_tags_{item.id}",
            )

            submitted = st.form_submit_button("Save")
            if submitted:
                if not title.strip():
                    st.warning("Title is required.")
                else:
                    repo = get_repo()
                    updated = update_todo(
                        repo=repo,
                        item_id=item.id or 0,
                        title=title,
                        description=description,
                        due_date=due_date_value,
                        priority=priority,
                        tags=_parse_tags(tags_raw),
                    )
                    if updated is not None:
                        st.success("TODO updated.")
                    else:
                        st.error("TODO not found. It may have been deleted.")


def _render_todo_row(item: TodoItem) -> None:
    """Render a single TODO row.

    Args:
        item: TODO item to render.
    """
    cols = st.columns([0.1, 0.9])
    with cols[0]:
        st.checkbox(
            label="Done",
            value=item.status == Status.DONE,
            key=f"todo_checkbox_{item.id}",
            label_visibility="collapsed",
            on_change=_on_toggle,
            args=(item.id or 0,),
        )

    with cols[1]:
        title_text = item.title
        if item.status == Status.DONE:
            title_text = f"~~{title_text}~~"
        st.markdown(f"**{title_text}**")

        meta_parts: list[str] = []
        if item.due_date:
            meta_parts.append(f"Due: {item.due_date.isoformat()}")
        if item.priority:
            meta_parts.append(f"Priority: {_priority_enum_to_label(item.priority)}")
        if item.tags:
            meta_parts.append(f"Tags: {', '.join(item.tags)}")

        if meta_parts:
            st.caption(" | ".join(meta_parts))

        if item.description:
            st.write(item.description)

        _render_edit_form(item)


def main() -> None:
    """Main entrypoint for the Streamlit TODO app."""
    st.set_page_config(page_title="TODO App", page_icon="✅")
    st.title("TODO App")

    # Ensure database schema exists.
    init_db()

    render_create_form()
    st.divider()

    status_filter, priority_filter, due_today_or_overdue = render_filters()
    st.divider()

    render_todo_list(
        status_filter=status_filter,
        priority_filter=priority_filter,
        due_today_or_overdue=due_today_or_overdue,
    )


if __name__ == "__main__":
    main()
