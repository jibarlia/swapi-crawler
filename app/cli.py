import typer
from sqlmodel import Session

import app.models  # noqa: F401 — registers all models with SQLModel.metadata
from app.clients.public_api_client import SWAPIClient
from app.db import create_db_and_tables, drop_db_and_tables, engine
from app.services.crawler_service import CrawlerService

cli = typer.Typer(name="swapi-crawler")


@cli.command()
def crawl():
    """Fetch all SWAPI entities and upsert them into the database."""
    create_db_and_tables()
    with Session(engine) as session:
        with SWAPIClient() as client:
            counts = CrawlerService(client=client, session=session).crawl()
    for entity, count in counts.items():
        typer.echo(f"  {entity}: {count} upserted")


@cli.command(name="reset-db")
def reset_db():
    """Drop and recreate all database tables."""
    typer.confirm("This will drop all data. Continue?", abort=True)
    drop_db_and_tables()
    create_db_and_tables()
    typer.echo("Database reset complete.")


if __name__ == "__main__":
    cli()
