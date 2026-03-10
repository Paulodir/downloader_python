from __future__ import annotations

from typing import Any

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Vaga(TimestampMixin, Base):
    __tablename__ = "vagas"

    id: Mapped[int] = mapped_column(primary_key=True)
    edital_id: Mapped[int] = mapped_column(ForeignKey("editais.id", ondelete="CASCADE"), index=True)
    modalidade_id: Mapped[int | None] = mapped_column(
        ForeignKey("modalidades.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    codigo: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    descricao: Mapped[str | None] = mapped_column(Text(), nullable=True)
    quantidade: Mapped[int | None] = mapped_column(nullable=True)
    turno: Mapped[str | None] = mapped_column(String(100), nullable=True)
    local: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    edital = relationship("Edital", back_populates="vagas", overlaps="modalidades,vagas")
    modalidade = relationship("Modalidade", back_populates="vagas")
    anexos = relationship(
        "Anexo",
        back_populates="vaga",
        cascade="all, delete-orphan",
        overlaps="edital,anexos",
    )
