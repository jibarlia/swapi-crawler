from typing import Optional, Type

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, SQLModel, select


class BaseRepository:
    model: Type[SQLModel]

    def __init__(self, session: Session):
        self._session = session

    def upsert_batch(self, records: list[dict]) -> int:
        if not records:
            return 0
        insert_stmt = pg_insert(self.model).values(records)
        update_cols = {c: insert_stmt.excluded[c] for c in records[0] if c != "id"}
        stmt = insert_stmt.on_conflict_do_update(
            index_elements=["id"], set_=update_cols
        )
        self._session.exec(stmt)
        self._session.commit()
        # on_conflict_do_update writes every record (insert or update), so the
        # affected count is just the batch size — psycopg reports rowcount as -1
        # for multi-row upserts, which isn't usable.
        return len(records)

    def get_all(self, offset: int = 0, limit: int = 20) -> list:
        return list(
            self._session.exec(
                select(self.model).offset(offset).limit(limit).order_by(self.model.id)
            ).all()
        )

    def get_by_id(self, entity_id: int) -> Optional[SQLModel]:
        return self._session.get(self.model, entity_id)

    def count(self) -> int:
        return self._session.exec(select(func.count()).select_from(self.model)).one()
