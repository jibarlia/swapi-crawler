from datetime import datetime

from sqlalchemy import Column, DateTime, Text, func
from sqlmodel import Field, SQLModel


class Film(SQLModel, table=True):
    __tablename__ = "films"

    id: int = Field(primary_key=True)
    title: str
    episode_id: int | None = None
    opening_crawl: str | None = Field(default=None, sa_column=Column(Text))
    director: str | None = None
    producer: str | None = None
    release_date: str | None = None
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
