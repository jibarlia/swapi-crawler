import pytest
from sqlmodel import Session, SQLModel, create_engine, delete

import app.models  # noqa: F401 — registers all models before create_all
from app.models.film import Film
from app.models.links import (
    FilmPlanet,
    FilmSpecies,
    FilmStarship,
    FilmVehicle,
    PersonFilm,
    PersonSpecies,
    PersonStarship,
    PersonVehicle,
)
from app.models.person import Person
from app.models.planet import Planet
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle

TEST_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/crawler_test_db"

_LINK_MODELS = [
    PersonFilm,
    PersonSpecies,
    PersonVehicle,
    PersonStarship,
    FilmPlanet,
    FilmVehicle,
    FilmStarship,
    FilmSpecies,
]
_ENTITY_MODELS = [Person, Film, Planet, Species, Vehicle, Starship]


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def session(test_engine):
    with Session(test_engine) as s:
        yield s


@pytest.fixture(autouse=True)
def clean_tables(test_engine):
    yield
    with Session(test_engine) as s:
        for model in _LINK_MODELS + _ENTITY_MODELS:
            s.exec(delete(model))
        s.commit()
