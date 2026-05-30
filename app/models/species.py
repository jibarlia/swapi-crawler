from sqlmodel import Field

from app.models.mixins import TimestampMixin


class Species(TimestampMixin, table=True):
    __tablename__ = "species"

    id: int = Field(primary_key=True)
    name: str
    classification: str | None = None
    designation: str | None = None
    average_height: str | None = None
    skin_colors: str | None = None
    hair_colors: str | None = None
    eye_colors: str | None = None
    average_lifespan: str | None = None
    homeworld_id: int | None = None
    language: str | None = None
    url: str | None = None
