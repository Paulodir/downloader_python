from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.vaga import Vaga


class VagaRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_by_edital(self, edital_id: int) -> list[Vaga]:
        statement = select(Vaga).where(Vaga.edital_id == edital_id).order_by(Vaga.titulo.asc())
        return self.session.scalars(statement).all()

    def save(self, vaga: Vaga) -> Vaga:
        self.session.add(vaga)
        self.session.flush()
        return vaga

    def delete_by_edital_id(self, edital_id: int) -> None:
        self.session.execute(delete(Vaga).where(Vaga.edital_id == edital_id))
