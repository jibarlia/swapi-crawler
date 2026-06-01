# Public API Crawler Template

Reusable backend boilerplate for interview exercises involving:

- Public API integrations
- Crawlers/importers
- Entity modeling
- Database persistence
- CLI commands
- Optional REST API exposure

Built with:

- FastAPI
- SQLModel
- Typer
- SQLite
- HTTPX
- Pytest

---

# Project Structure

```txt
app/
  clients/        # External API clients
  models/         # SQLModel entities
  repositories/   # Database access layer
  services/       # Business logic
  cli.py          # CLI commands
  main.py         # FastAPI app
  db.py           # Database/session config
```

---

# Setup

## Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate

uv venv
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Formatting with Ruff

```bash
uv run ruff check
uv run ruff check . --fix
uv run ruff format .

ruff format path/to/file
```

---

# Running FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```txt
http://127.0.0.1:8000/docs
```

---

# First Run

On a fresh database, create the schema before crawling:

```bash
python -m app.cli init-db   # create tables (run once)
python -m app.cli crawl     # fetch + persist entities
```

> The FastAPI app also creates the schema automatically on startup, so if
> you've already run `uvicorn app.main:app` you can skip `init-db`.

---

# CLI Examples

## Initialize the database schema

```bash
python -m app.cli init-db
```

## Crawl entities

```bash
python -m app.cli crawl
```

## Reset database

```bash
python -m app.cli reset-db
```

---

# Running Tests

```bash
pytest
```

---

# Goals of this Template

This repository is intended for:

- Backend interview practice
- Public API exercises
- Entity modeling practice
- FastAPI/SQLModel experimentation
- Reusable coding challenge starter

---

# Future Improvements

- PostgreSQL support
- Alembic migrations
- Async DB support
- Docker setup
- Background workers
- Pagination utilities
- Retry decorators
- Caching layer