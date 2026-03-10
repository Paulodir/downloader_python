from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.inscricao import Inscricao


class InscricaoRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Inscricao]:
        return self.session.scalars(select(Inscricao)).all()

    def save(self, inscricao: Inscricao) -> Inscricao:
        self.session.add(inscricao)
        self.session.flush()
        return inscricao

    def delete_by_edital_id(self, edital_id: int) -> None:
        self.session.execute(delete(Inscricao).where(Inscricao.edital_id == edital_id))
