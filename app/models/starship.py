from sqlmodel import Field

from app.models.mixins import TimestampMixin


class Starship(TimestampMixin, table=True):
    __tablename__ = "starships"

    id: int = Field(primary_key=True)
    name: str
    model: str | None = None
    manufacturer: str | None = None
    cost_in_credits: str | None = None
    length: str | None = None
    max_atmosphering_speed: str | None = None
    crew: str | None = None
    passengers: str | None = None
    cargo_capacity: str | None = None
    consumables: str | None = None
    hyperdrive_rating: str | None = None
    mglt: str | None = None
    starship_class: str | None = None
    url: str | None = None
