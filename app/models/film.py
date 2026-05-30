from sqlalchemy import Column, Text
from sqlmodel import Field

from app.models.mixins import TimestampMixin


class Film(TimestampMixin, table=True):
    __tablename__ = "films"

    id: int = Field(primary_key=True)
    title: str
    episode_id: int | None = None
    opening_crawl: str | None = Field(default=None, sa_column=Column(Text))
    director: str | None = None
    producer: str | None = None
    release_date: str | None = None
    url: str | None = None
