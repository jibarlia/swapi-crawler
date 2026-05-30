from sqlmodel import Field

from app.models.mixins import TimestampMixin


class Vehicle(TimestampMixin, table=True):
    __tablename__ = "vehicles"

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
    vehicle_class: str | None = None
    url: str | None = None
