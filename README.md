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
```

## Install dependencies

```bash
pip install -r requirements.txt
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

# CLI Examples

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