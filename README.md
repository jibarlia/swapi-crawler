# SWAPI Crawler

A crawler for the **Star Wars API ([swapi.info](https://swapi.info/api))**. It fetches all SWAPI
entities, persists them into a relational PostgreSQL schema, and exposes them through a
Typer CLI and a FastAPI REST API.

Entities: **people, films, planets, species, vehicles, starships**, plus the many-to-many
relationships between them (e.g. people ↔ films, films ↔ planets).

> The project follows a clean layered architecture
> (cli → service → repository → db)
> and can serve as a foundation for similar public API ingestion projects.

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

This project uses **[uv](https://docs.astral.sh/uv/)**. Dependencies live in `pyproject.toml`
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

### Running commands

There are two equally valid styles — pick one:

- **Don't activate anything** — prefix commands with `uv run`, which auto-syncs and uses the
project venv:
  ```bash
  uv run python -m app.cli crawl
  uv run pytest
  ```
- **Activate the venv** if you prefer a bare `python` / `pytest`:
  ```bash
  source .venv/bin/activate
  ```

The rest of this README uses the `uv run` form.

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

GET /films
GET /planets
GET /species
GET /vehicles
GET /starships
```

People also expose their relationships and a composite detail view:

```txt
GET /people/{id}/films
GET /people/{id}/starships
GET /people/{id}/vehicles
GET /people/{id}/species
GET /people/{id}/details    # person + nested homeworld, films, starships, vehicles, species
```

Example `GET /people/1/details` (abbreviated):

```json
{
  "id": 1,
  "name": "Luke Skywalker",
  "height": "172",
  "mass": "77",
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color": "blue",
  "birth_year": "19BBY",
  "gender": "male",
  "url": "https://swapi.info/api/people/1",
  "created_at": "2014-12-09T13:50:51.644000+00:00",
  "updated_at": "2014-12-20T21:17:56.891000+00:00",
  "homeworld": {
    "id": 1,
    "name": "Tatooine",
    "climate": "arid",
    "terrain": "desert",
    "population": "200000",
    "url": "https://swapi.info/api/planets/1"
  },
  "films": [
    { "id": 1, "title": "A New Hope", "episode_id": 4, "release_date": "1977-05-25" }
  ],
  "starships": [
    { "id": 12, "name": "X-wing", "model": "T-65 X-wing", "starship_class": "Starfighter" }
  ],
  "vehicles": [
    { "id": 14, "name": "Snowspeeder", "vehicle_class": "airspeeder" }
  ],
  "species": []
}
```

> Nested objects include all their model fields; only a subset is shown above for brevity.
> `homeworld` is `null` when the person has none, and each relation list is `[]` when empty.

---

## Docker

Run the whole stack (PostgreSQL + the FastAPI app) with Docker — no local `uv` or
Postgres needed.

```bash
# Full stack (Postgres + app) via compose
docker compose up -d --build        # starts Postgres + API at http://localhost:8000
docker compose run --rm app uv run python -m app.cli crawl   # one-off crawl
docker compose down                 # stop (add -v to also wipe the DB volume)
```

Swagger UI is at `http://localhost:8000/docs`. The schema is created automatically on
app startup, so there's no need to run `init-db` under compose.

To build and run the image on its own (point it at a reachable Postgres):

```bash
docker build -t swapi-crawler .
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://postgres:postgres@host.docker.internal:5432/swapi \
  swapi-crawler
```

---

## Development

```bash
uv run pytest                       # run the unit suite (no database required)
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
- Retry/backoff in the SWAPI client
- Integration tests for the repository layer against a real test database

