from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.edital import Edital


class EditalRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> Sequence[Edital]:
        statement = select(Edital).order_by(
            Edital.synced_at.is_(None),
            Edital.synced_at.desc(),
            Edital.codigo.asc(),
        )
        return self.session.scalars(statement).all()

    def get_by_id(self, edital_id: int) -> Edital | None:
        return self.session.get(Edital, edital_id)

    def get_by_codigo(self, codigo: str) -> Edital | None:
        statement = select(Edital).where(Edital.codigo == codigo)
        return self.session.scalar(statement)

    def save(self, edital: Edital) -> Edital:
        self.session.add(edital)
        self.session.flush()
        return edital
