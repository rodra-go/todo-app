# TODO App (Streamlit + SQLite)

Simple single-user TODO app with a Streamlit UI and SQLite persistence.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Run the app

```bash
streamlit run src/todo_app/ui/streamlit_app.py
```

## Run tests

```bash
pytest
```

## Run lint and formatting checks

```bash
ruff check src tests
black --check src tests
mypy src
```

