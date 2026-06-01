# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

`swapi-crawler` crawls the **Star Wars API ([swapi.info](https://swapi.info/api))**, persists its entities into a relational PostgreSQL schema, and exposes them via a Typer CLI and a FastAPI REST API.

It started from a reusable public-API crawler boilerplate, but is now a concrete SWAPI implementation. The layered structure is still generic enough to fork as a base for another public-API exercise, but new code should be SWAPI-specific where that keeps things simpler.

## Tooling & Commands

This project uses **[uv](https://docs.astral.sh/uv/)** for environment and dependency management. Dependencies live in `pyproject.toml` (`[project.dependencies]` for runtime, `[dependency-groups].dev` for dev); `uv.lock` pins exact versions. There is no `requirements.txt`.

```bash
# Install/sync the environment (creates .venv from uv.lock)
uv sync                 # runtime deps only
uv sync --all-groups    # include dev deps (pytest, ruff, pre-commit)

# Add / remove dependencies (updates pyproject.toml + uv.lock)
uv add <package>
uv add --dev <package>
uv remove <package>

# Run anything inside the project environment
uv run uvicorn app.main:app --reload   # FastAPI dev server (Swagger at /docs)
uv run python -m app.cli init-db        # create tables (run once on a fresh DB)
uv run python -m app.cli crawl          # fetch SWAPI + upsert
uv run python -m app.cli reset-db       # drop + recreate all tables

# Tests
uv run pytest
uv run pytest tests/test_crawler_service.py
uv run pytest tests/test_crawler_service.py::TestTransformPerson

# Lint / format
uv run ruff check . --fix
uv run ruff format .
```

> Need a pip-style export for a non-uv environment? `uv export --no-dev -o requirements.txt`.

## Architecture

The layered structure enforces a strict dependency direction: `cli/main → service → repository → db`, with the SWAPI client injected into the crawler service.

| Layer | Path | Role |
|---|---|---|
| Config | `app/config.py` | Env vars via `environs`; `DATABASE_URL`, `DEBUG`, `APP_NAME` |
| DB | `app/db.py` | SQLModel engine + session factory and schema create/drop (PostgreSQL via `psycopg` v3) |
| Models | `app/models/` | One SQLModel table per entity (`person`, `film`, `planet`, `species`, `vehicle`, `starship`), `links.py` for many-to-many join tables, `mixins.py` for `TimestampMixin` |
| Client | `app/clients/public_api_client.py` | `SWAPIClient` — HTTPX client fetching each `swapi.info` collection |
| Repository | `app/repositories/` | Data access only. `base_repository.py` (generic upsert/get/count via `model = X`), `link_repository.py` (join-table upserts), per-entity subclasses |
| Service | `app/services/crawler_service.py` | Orchestrates fetch → transform → upsert, including the link/join tables |
| Service | `app/services/entity_service.py` | Read-side queries (list/get per entity) for CLI and API |
| CLI | `app/cli.py` | Typer commands: `init-db`, `crawl`, `reset-db` |
| API | `app/main.py` | FastAPI app; `GET` list/detail endpoints per entity; schema bootstrap via `lifespan` |

## Key Conventions

- `app/config.py` is the single source of truth for env vars — never read `os.environ` directly elsewhere.
- `.env.example` documents required env vars; `.env` is gitignored.
- Database is **PostgreSQL** via `psycopg` (v3); `DATABASE_URL` uses the `postgresql+psycopg://` scheme.
- Schema lifecycle is explicit: `init-db` / `reset-db` own DDL; the API `lifespan` also bootstraps tables on startup. `crawl` assumes the schema exists.
- Models use **SQLModel**. SWAPI exposes related entities as URLs; the crawler extracts integer IDs from those URLs and resolves relationships into FK columns and join tables.
- The repository layer owns all SQL — services must not write raw queries; repositories must not hold business logic.
- `upsert_batch` uses Postgres `INSERT ... ON CONFLICT DO UPDATE` and returns `len(records)` (psycopg reports `-1` for multi-row upserts).
- Use `session.exec()` (not the deprecated `session.execute()`).
- Tests live in `tests/` and follow `test_*.py`. Mock the SWAPI client with `pytest-mock`. (Known gap: some logic-only tests currently pull in a DB-bound fixture — to be decoupled.)
