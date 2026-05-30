from typing import Type

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, SQLModel


class BaseLinkRepository:
    model: Type[SQLModel]
    pk_columns: list[str]

    def __init__(self, session: Session):
        self._session = session

    def upsert_batch(self, pairs: list[dict]) -> None:
        if not pairs:
            return
        stmt = pg_insert(self.model).values(pairs).on_conflict_do_nothing(index_elements=self.pk_columns)
        self._session.execute(stmt)
        self._session.commit()
