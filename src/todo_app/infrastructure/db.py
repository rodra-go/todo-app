from __future__ import annotations

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def get_engine() -> Engine:
    """Create or retrieve the SQLAlchemy engine.

    Returns:
        A SQLAlchemy engine bound to a local SQLite database file.
    """
    # Local file `todo.db` in project root.
    return create_engine("sqlite:///todo.db", echo=False, future=True)


def get_session_factory() -> sessionmaker[Session]:
    """Return a configured session factory.

    Returns:
        A SQLAlchemy sessionmaker bound to the application engine.
    """
    engine = get_engine()
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=Session,
    )


def _run_migrations(engine: Engine) -> None:
    """Apply simple in-place migrations for the SQLite schema.

    This is intentionally minimal and only handles adding new nullable
    columns to the existing `todos` table.
    """
    insp = inspect(engine)
    if not insp.has_table("todos"):
        # Table does not exist yet; `create_all` will create it.
        return

    existing_cols = {col["name"] for col in insp.get_columns("todos")}

    # We only ever ADD nullable columns so existing data stays valid.
    with engine.begin() as conn:
        if "due_date" not in existing_cols:
            conn.execute(text("ALTER TABLE todos ADD COLUMN due_date DATE"))
        if "priority" not in existing_cols:
            conn.execute(text("ALTER TABLE todos ADD COLUMN priority VARCHAR(20)"))
        if "tags" not in existing_cols:
            conn.execute(text("ALTER TABLE todos ADD COLUMN tags VARCHAR(255)"))


def init_db() -> None:
    """Initialize the database schema and run lightweight migrations."""
    # Import ORM models so metadata is populated.
    from . import models as orm_models  # noqa: F401

    engine = get_engine()
    _run_migrations(engine)
    Base.metadata.create_all(bind=engine)
