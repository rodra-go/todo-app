from __future__ import annotations

from typing import Optional

import streamlit as st

from todo_app.domain.models import Status, TodoItem
from todo_app.domain.services import create_todo, list_todos, toggle_done
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


def render_create_form() -> None:
    """Render the form to create a new TODO item."""
    st.subheader("Add TODO")
    with st.form("create_todo_form", clear_on_submit=True):
        title: str = st.text_input("Title", "")
        description: str = st.text_area("Description", "")
        submitted = st.form_submit_button("Add")
        if submitted:
            if not title.strip():
                st.warning("Title is required.")
            else:
                repo = get_repo()
                create_todo(repo=repo, title=title, description=description)
                st.success("TODO created.")


def render_todo_list() -> None:
    """Render the list of existing TODO items with toggle actions."""
    st.subheader("TODOs")

    repo = get_repo()
    items = list_todos(repo=repo)

    if not items:
        st.info("No TODOs yet. Add one above.")
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
        if item.description:
            st.caption(item.description)


def main() -> None:
    """Main entrypoint for the Streamlit TODO app."""
    st.set_page_config(page_title="TODO App", page_icon="✅")
    st.title("TODO App")

    # Ensure database schema exists.
    init_db()

    render_create_form()
    st.divider()
    render_todo_list()


if __name__ == "__main__":
    main()
