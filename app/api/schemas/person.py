from datetime import datetime

from sqlmodel import SQLModel

from app.models.film import Film
from app.models.planet import Planet
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle


class PersonDetails(SQLModel):
    """A person with its relationships resolved into nested objects.

    Person scalar fields are re-declared here (rather than inheriting from the
    ``table=True`` Person) so the response is a plain schema; ``homeworld_id`` is
    replaced by the nested ``homeworld``.
    """

    id: int
    name: str
    height: str | None = None
    mass: str | None = None
    hair_color: str | None = None
    skin_color: str | None = None
    eye_color: str | None = None
    birth_year: str | None = None
    gender: str | None = None
    url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    homeworld: Planet | None = None
    films: list[Film] = []
    starships: list[Starship] = []
    vehicles: list[Vehicle] = []
    species: list[Species] = []
