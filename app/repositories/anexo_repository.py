from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.anexo import Anexo


class AnexoRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_by_edital(self, edital_id: int) -> list[Anexo]:
        statement = select(Anexo).where(Anexo.edital_id == edital_id).order_by(Anexo.nome.asc())
        return self.session.scalars(statement).all()

    def save(self, anexo: Anexo) -> Anexo:
        self.session.add(anexo)
        self.session.flush()
        return anexo

    def delete_by_edital_id(self, edital_id: int) -> None:
        self.session.execute(delete(Anexo).where(Anexo.edital_id == edital_id))
