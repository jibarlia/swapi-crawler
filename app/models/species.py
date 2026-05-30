from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Species(SQLModel, table=True):
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
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
    )
