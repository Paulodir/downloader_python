from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.modalidade import Modalidade


class ModalidadeRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_by_edital(self, edital_id: int) -> list[Modalidade]:
        statement = select(Modalidade).where(Modalidade.edital_id == edital_id).order_by(Modalidade.nome.asc())
        return self.session.scalars(statement).all()

    def save(self, modalidade: Modalidade) -> Modalidade:
        self.session.add(modalidade)
        self.session.flush()
        return modalidade

    def delete_by_edital_id(self, edital_id: int) -> None:
        self.session.execute(delete(Modalidade).where(Modalidade.edital_id == edital_id))
