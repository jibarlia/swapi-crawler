from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Person(SQLModel, table=True):
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
