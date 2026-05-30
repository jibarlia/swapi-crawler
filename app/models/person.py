from sqlmodel import Field

from app.models.mixins import TimestampMixin


class Person(TimestampMixin, table=True):
    __tablename__ = "people"

    id: int = Field(primary_key=True)
    name: str
    height: str | None = None
    mass: str | None = None
    hair_color: str | None = None
    skin_color: str | None = None
    eye_color: str | None = None
    birth_year: str | None = None
    gender: str | None = None
    homeworld_id: int | None = None
    url: str | None = None
