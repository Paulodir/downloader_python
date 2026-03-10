from __future__ import annotations

from typing import Any

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Anexo(TimestampMixin, Base):
    __tablename__ = "anexos"

    id: Mapped[int] = mapped_column(primary_key=True)
    edital_id: Mapped[int] = mapped_column(ForeignKey("editais.id", ondelete="CASCADE"), index=True)
    vaga_id: Mapped[int | None] = mapped_column(
        ForeignKey("vagas.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    inscricao_id: Mapped[int | None] = mapped_column(
        ForeignKey("inscricoes.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    categoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("categorias.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    subgrupo_id: Mapped[int | None] = mapped_column(
        ForeignKey("subgrupos.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    codigo: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    tipo_documento: Mapped[str | None] = mapped_column(String(64), nullable=True)
    extensao: Mapped[str | None] = mapped_column(String(20), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    edital = relationship("Edital", back_populates="anexos", overlaps="vaga,anexos")
    vaga = relationship("Vaga", back_populates="anexos", overlaps="edital,anexos")
    inscricao = relationship("Inscricao", back_populates="anexos")
    categoria = relationship("Categoria", back_populates="anexos")
    subgrupo = relationship("Subgrupo", back_populates="anexos")
    documentos = relationship(
        "Documento",
        back_populates="anexo",
        cascade="all, delete-orphan",
    )
