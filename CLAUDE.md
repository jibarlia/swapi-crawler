# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a reusable Python boilerplate for backend interview exercises that involve a public API integration. Each exercise instantiates this template with a concrete API target and entity domain. The goal is a working crawler that fetches data from a public API, persists it to a PostgreSQL database, and exposes it via CLI and optionally via a REST API.

## Commands

```bash
# Create and activate virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI dev server
uvicorn app.main:app --reload

# Run CLI commands
python -m app.cli crawl
python -m app.cli reset-db

# Run all tests
pytest

# Run a single test file or test
pytest tests/test_crawler_service.py
pytest tests/test_crawler_service.py::test_fetch_entities
```

## Architecture

The layered structure enforces a strict dependency direction: `cli/main → service → repository → db`, with the API client injected into the service layer.

| Layer | Path | Role |
|---|---|---|
| Config | `app/config.py` | Env vars via `environs`; `DATABASE_URL`, `DEBUG`, `APP_NAME` |
| DB | `app/db.py` | SQLModel engine and session factory (PostgreSQL via `psycopg`) |
| Models | `app/models/` | SQLModel table definitions (the crawled entity) |
| Client | `app/clients/public_api_client.py` | HTTPX-based client for the target public API |
| Repository | `app/repositories/entity_repository.py` | Raw DB access — upserts, queries |
| Service | `app/services/crawler_service.py` | Orchestrates fetch → transform → persist |
| Service | `app/services/entity_service.py` | Read-side queries exposed to CLI and API |
| CLI | `app/cli.py` | Typer commands (`crawl`, `reset-db`, etc.) |
| API | `app/main.py` | FastAPI app with REST endpoints |

## Key Conventions

- `app/config.py` is the single source of truth for env vars — never read `os.environ` directly elsewhere.
- `.env.example` documents required env vars; `.env` is gitignored.
- Database is **PostgreSQL** accessed via `psycopg` (v3). The `DATABASE_URL` uses the `postgresql+psycopg://` scheme.
- Models use **SQLModel** (combines SQLAlchemy + Pydantic). Table models go in `app/models/`, response schemas can be colocated or separated.
- The repository layer owns all SQL; services must not write raw queries.
- Tests live in `tests/` and follow the `test_*.py` naming convention. Use `pytest-mock` to mock the API client; hit a real (test) database for repository tests.
