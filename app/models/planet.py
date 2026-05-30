from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Planet(SQLModel, table=True):
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
