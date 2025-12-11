# TODO App

A clean, testable, local TODO / checklist application built in under 60 minutes,
following solid engineering principles and a layered architecture.

## 🚀 Project Overview

This project is a lightweight personal TODO application designed to demonstrate:

- Clean modular architecture (domain → infrastructure → UI)
- Strong typing and documentation standards
- Testability and CI integration
- Use of modern Python tooling (ruff, black, mypy, pytest)
- A functional UI built with Streamlit

## ✨ Features

- Create TODO items with:
  - Title and description
  - Optional due date
  - Optional priority (Low / Medium / High)
  - Optional list of tags
- Mark items done/undone
- Edit existing items inline
- Filters:
  - Status (All / Pending / Done)
  - Priority
  - "Due today or overdue"
- Persistent storage with SQLite + SQLAlchemy
- Automatic schema “migration” for new columns
- Full test suite for domain logic and persistence
- CI pipeline running ruff, black, mypy, and pytest

## 🏗️ Architecture

```text
src/todo_app/
├── domain/          # Pure business logic, independent of frameworks
│   ├── models.py
│   ├── repositories.py
│   ├── services.py
├── infrastructure/  # DB engine, ORM models, SQLAlchemy repository
│   ├── db.py
│   ├── models.py
│   ├── repositories.py
├── ui/              # Streamlit UI layer (no business logic)
│   ├── streamlit_app.py
│   ├── helpers.py
```

### Domain layer
Defines the `TodoItem` entity, enums, and business logic.  
No reference to SQLAlchemy, Streamlit, or persistence concerns.

### Infrastructure layer
SQLAlchemy ORM models and the repository implementation.  
Lightweight migration inside `init_db()` ensures schema stays up-to-date.

### UI layer
Streamlit app calling domain services and repository methods.  
Presents forms, filtering UI, and edit widgets.

## 🔧 Installation

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e .[dev]
```

## ▶️ Running the App

```bash
streamlit run src/todo_app/ui/streamlit_app.py
```

A todo.db file will be created automatically on first launch.

## 🧪 Running Tests

```bash
pytest
```

Tests include:

- Domain logic tests using an in-memory repository
- SQLAlchemy repository tests using a temporary SQLite DB

## 🧹 Linting & Formatting

Ruff (linting)

```bash
ruff check src tests
```

Black (formatting)

```bash
black src tests
```

Check only:

```bash
black --check src tests
```

## 🔍 Static Type Checking (mypy)

```bash
mypy src tests
```

## 🔄 Running CI Locally

The CI pipeline (GitHub Actions) runs:

- ruff
- black --check
- mypy
- pytest

Reproduce locally:

```bash
ruff check src tests
black --check src tests
mypy src tests
pytest
```
## 📦 CI/CD

GitHub Actions workflow located at:

```
.github/workflows/CI.yml
```

It automatically runs on each push or pull request.

## 📝 Validation Checklist Before Packaging

Manual pre-submission checks:

```bash
ruff check src tests
black --check src tests
mypy src tests
pytest
streamlit run src/todo_app/ui/streamlit_app.py
```

Then validate UI manually:

1. Create a TODO with title, description, priority, due date, tags.
2. Confirm it appears in the list.
3. Toggle DONE/UNDONE.
4. Edit the TODO and confirm changes persist.
5. Test filters:
   - Status filter (Pending / Done / All)
   - Priority filter
   - Due today/overdue
6. Restart the app — data should still be present in todo.db.

If all steps pass, the submission is ready.