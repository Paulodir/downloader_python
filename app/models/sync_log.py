from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    edital_id: Mapped[int | None] = mapped_column(
        ForeignKey("editais.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    categoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("categorias.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    codigo_edital: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    tipo_documento: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="started")
    message: Mapped[str | None] = mapped_column(Text(), nullable=True)
    payload_summary: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)

    edital = relationship("Edital", back_populates="sync_logs")
    categoria = relationship("Categoria", back_populates="sync_logs")
