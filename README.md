# TODO App

Simple local TODO / checklist app built with:

- Python 3.12
- Streamlit (UI)
- SQLite + SQLAlchemy (persistence)
- pytest (tests)
- ruff + black (lint/format)
- GitHub Actions (CI)

## Installation

Create and activate a virtual environment, then install the package:

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e .[dev]
```

## Running the App

From the project root:

```bash
streamlit run src/todo_app/ui/streamlit_app.py
```

This will create a `todo.db` SQLite file in the project directory.

## Linting and Formatting

Run black (format):

```bash
black src tests
```

Or to just check formatting without modifying files:

```bash
black --check src tests
```

Run ruff (lint):

```bash
ruff check src tests
```

## Type checking (mypy)

Run mypy over the source and tests:

```bash
mypy src tests
```

# Tests

Run the test suite with:

```bash
pytest
```

## CI

A GitHub Actions workflow (`.github/workflows/CI.yml`) is provided. It:

- Sets up Python 3.12
- Installs dependencies (pip install -e .[dev])
- Runs ruff check
- Runs black --check
- Runs pytest