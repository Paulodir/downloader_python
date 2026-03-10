from __future__ import annotations

from typing import Any

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Documento(TimestampMixin, Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    anexo_id: Mapped[int | None] = mapped_column(
        ForeignKey("anexos.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    descricao: Mapped[str | None] = mapped_column(Text(), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    anexo = relationship("Anexo", back_populates="documentos")
