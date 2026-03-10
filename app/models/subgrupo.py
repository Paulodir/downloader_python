from __future__ import annotations

from typing import Any

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Subgrupo(TimestampMixin, Base):
    __tablename__ = "subgrupos"

    id: Mapped[int] = mapped_column(primary_key=True)
    grupo_id: Mapped[int | None] = mapped_column(
        ForeignKey("grupos.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    descricao: Mapped[str | None] = mapped_column(Text(), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    grupo = relationship("Grupo", back_populates="subgrupos")
    anexos = relationship("Anexo", back_populates="subgrupo")
