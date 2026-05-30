from sqlmodel import Field

from app.models.mixins import TimestampMixin


class Planet(TimestampMixin, table=True):
    __tablename__ = "planets"

    id: int = Field(primary_key=True)
    name: str
    rotation_period: str | None = None
    orbital_period: str | None = None
    diameter: str | None = None
    climate: str | None = None
    gravity: str | None = None
    terrain: str | None = None
    surface_water: str | None = None
    population: str | None = None
    url: str | None = None
