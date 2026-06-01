# SWAPI Crawler

A crawler for the **Star Wars API ([swapi.info](https://swapi.info/api))**. It fetches all SWAPI
entities, persists them into a relational PostgreSQL schema, and exposes them through a
Typer CLI and a FastAPI REST API.

Entities: **people, films, planets, species, vehicles, starships**, plus the many-to-many
relationships between them (e.g. people ↔ films, films ↔ planets).

> This started life as a generic public-API crawler boilerplate and keeps a clean layered
> structure (`cli/main → service → repository → db`), so it can still be forked as a base for
> another public-API exercise. From here on, though, it is SWAPI-specific.

Built with: **FastAPI · SQLModel · Typer · HTTPX · PostgreSQL (psycopg 3) · uv**

---

## Project Structure

```txt
app/
  clients/        # SWAPIClient (HTTPX)
  models/         # SQLModel entities, join tables (links.py), TimestampMixin (mixins.py)
  repositories/   # Data access — base/link repositories + per-entity subclasses
  services/       # crawler_service (fetch→transform→upsert), entity_service (reads)
  cli.py          # Typer commands: init-db, crawl, reset-db
  main.py         # FastAPI app + REST endpoints
  config.py       # Env vars via environs
  db.py           # Engine, session factory, schema create/drop
```

---

## Setup

This project uses [**uv**](https://docs.astral.sh/uv/). Dependencies live in `pyproject.toml`
and are pinned in `uv.lock` — there is no `requirements.txt`.

```bash
# Install uv (if needed): https://docs.astral.sh/uv/getting-started/installation/

# Create the virtualenv and install everything (incl. dev tools)
uv sync --all-groups

# Configure environment
cp .env.example .env   # then edit DATABASE_URL to point at your Postgres
```

You need a running **PostgreSQL** instance. `DATABASE_URL` uses the `postgresql+psycopg://`
scheme, e.g.:

```txt
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/swapi
```

---

## First Run

On a fresh database, create the schema before crawling:

```bash
uv run python -m app.cli init-db   # create tables (run once)
uv run python -m app.cli crawl     # fetch SWAPI + persist
```

`crawl` is idempotent — re-running it upserts, refreshing existing rows in place.

> The FastAPI app also creates the schema on startup, so if you've already run the server
> you can skip `init-db`.

---

## CLI

```bash
uv run python -m app.cli init-db    # create all tables
uv run python -m app.cli crawl      # fetch all SWAPI entities and upsert them
uv run python -m app.cli reset-db   # drop and recreate all tables
```

---

## REST API

```bash
uv run uvicorn app.main:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

Each entity exposes a paginated list and a detail endpoint, e.g.:

```txt
GET /people            ?offset=0&limit=20
GET /people/{id}
GET /films  /planets  /species  /vehicles  /starships   (same shape)
```

---

## Development

```bash
uv run pytest                       # run tests
uv run ruff check . --fix           # lint + autofix
uv run ruff format .                # format

uv add <package>                    # add a runtime dependency
uv add --dev <package>              # add a dev dependency
```

VS Code launch configurations are provided in `.vscode/launch.json` (FastAPI, Swagger,
CLI commands, pytest, Ruff).

---

## Future Improvements

- Alembic migrations
- Async DB support
- Docker / docker-compose for Postgres + app
- Retry/backoff in the SWAPI client
- Decouple logic-only tests from the database
