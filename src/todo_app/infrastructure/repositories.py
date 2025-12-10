from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from todo_app.domain.models import Status, TodoItem
from todo_app.domain.repositories import TodoRepository
from .models import TodoORM


class SqlAlchemyTodoRepository(TodoRepository):
    """SQLAlchemy-backed implementation of the TodoRepository protocol."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        """Initialize the repository.

        Args:
            session_factory: Factory used to create new SQLAlchemy sessions.
        """
        self._session_factory = session_factory

    def add(self, item: TodoItem) -> TodoItem:
        """Persist a new TODO item and return it with an assigned id."""
        with self._session_factory() as session:
            orm = TodoORM(
                title=item.title,
                description=item.description,
                status=item.status.name,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            session.add(orm)
            session.commit()
            session.refresh(orm)
            return self._to_domain(orm)

    def list_all(self) -> Sequence[TodoItem]:
        """Return all TODO items."""
        with self._session_factory() as session:
            stmt = select(TodoORM).order_by(TodoORM.created_at.desc())
            result = session.scalars(stmt).all()
            return [self._to_domain(row) for row in result]

    def get(self, item_id: int) -> Optional[TodoItem]:
        """Retrieve a TODO item by its id."""
        with self._session_factory() as session:
            orm = session.get(TodoORM, item_id)
            if orm is None:
                return None
            return self._to_domain(orm)

    def update(self, item: TodoItem) -> TodoItem:
        """Update an existing TODO item."""
        with self._session_factory() as session:
            orm = session.get(TodoORM, item.id)
            if orm is None:
                msg = f"Todo with id {item.id} not found"
                raise ValueError(msg)
            orm.title = item.title
            orm.description = item.description
            orm.status = item.status.name
            orm.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(orm)
            return self._to_domain(orm)

    def delete(self, item_id: int) -> None:
        """Delete a TODO item by its id."""
        with self._session_factory() as session:
            orm = session.get(TodoORM, item_id)
            if orm is None:
                return
            session.delete(orm)
            session.commit()

    def set_status(self, item_id: int, status: Status) -> Optional[TodoItem]:
        """Set the status of a TODO item and return the updated item."""
        with self._session_factory() as session:
            orm = session.get(TodoORM, item_id)
            if orm is None:
                return None
            orm.status = status.name
            orm.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(orm)
            return self._to_domain(orm)

    @staticmethod
    def _to_domain(orm: TodoORM) -> TodoItem:
        """Map ORM model to domain entity.

        Args:
            orm: ORM instance to convert.

        Returns:
            Domain-level TodoItem.
        """
        return TodoItem(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            status=Status[orm.status],
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
