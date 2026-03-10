from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.documento import Documento
from app.models.anexo import Anexo


class DocumentoRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_by_anexo(self, anexo_id: int) -> list[Documento]:
        statement = select(Documento).where(Documento.anexo_id == anexo_id).order_by(Documento.nome.asc())
        return self.session.scalars(statement).all()

    def save(self, documento: Documento) -> Documento:
        self.session.add(documento)
        self.session.flush()
        return documento

    def delete_by_edital_id(self, edital_id: int) -> None:
        subquery = select(Anexo.id).where(Anexo.edital_id == edital_id)
        self.session.execute(delete(Documento).where(Documento.anexo_id.in_(subquery)))
