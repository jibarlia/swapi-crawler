from typing import Type

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, SQLModel, select


class BaseLinkRepository:
    model: Type[SQLModel]
    pk_columns: list[str]

    def __init__(self, session: Session):
        self._session = session

    def upsert_batch(self, pairs: list[dict]) -> None:
        if not pairs:
            return
        stmt = (
            pg_insert(self.model)
            .values(pairs)
            .on_conflict_do_nothing(index_elements=self.pk_columns)
        )
        self._session.exec(stmt)
        self._session.commit()

    def get_related(
        self,
        source_col: str,
        source_id: int,
        target_model: Type[SQLModel],
        target_col: str,
    ) -> list:
        """Fetch target entities linked to ``source_id`` through this join table."""
        stmt = (
            select(target_model)
            .join(self.model, getattr(self.model, target_col) == target_model.id)
            .where(getattr(self.model, source_col) == source_id)
            .order_by(target_model.id)
        )
        return list(self._session.exec(stmt).all())
