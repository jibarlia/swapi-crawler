from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Starship(SQLModel, table=True):
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
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )
