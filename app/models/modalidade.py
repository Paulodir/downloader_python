from __future__ import annotations

from typing import Any

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Modalidade(TimestampMixin, Base):
    __tablename__ = "modalidades"

    id: Mapped[int] = mapped_column(primary_key=True)
    edital_id: Mapped[int] = mapped_column(ForeignKey("editais.id", ondelete="CASCADE"), index=True)
    codigo: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    descricao: Mapped[str | None] = mapped_column(Text(), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    edital = relationship("Edital", back_populates="modalidades")
    vagas = relationship(
        "Vaga",
        back_populates="modalidade",
        cascade="all, delete-orphan",
    )
