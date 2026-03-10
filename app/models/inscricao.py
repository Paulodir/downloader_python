from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Inscricao(TimestampMixin, Base):
    __tablename__ = "inscricoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    edital_id: Mapped[int | None] = mapped_column(
        ForeignKey("editais.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    vaga_id: Mapped[int | None] = mapped_column(
        ForeignKey("vagas.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pendente")
    inicio: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    fim: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    edital = relationship("Edital")
    vaga = relationship("Vaga")
