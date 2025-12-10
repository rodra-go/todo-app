from __future__ import annotations

from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def get_engine() -> "Engine":
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


def init_db() -> None:
    """Initialize the database schema if it does not exist."""
    from . import models as orm_models  # noqa: F401  # ensure models are imported

    engine = get_engine()
    Base.metadata.create_all(bind=engine)
