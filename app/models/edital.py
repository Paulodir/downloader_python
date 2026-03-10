from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Edital(TimestampMixin, Base):
    __tablename__ = "editais"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    descricao: Mapped[str | None] = mapped_column(Text(), nullable=True)
    tipo_documento: Mapped[str] = mapped_column(String(64), nullable=False)
    situacao: Mapped[str | None] = mapped_column(String(100), nullable=True)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    modalidades_count: Mapped[int] = mapped_column(default=0, nullable=False)
    vagas_count: Mapped[int] = mapped_column(default=0, nullable=False)
    anexos_count: Mapped[int] = mapped_column(default=0, nullable=False)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON(), nullable=True)

    modalidades = relationship(
        "Modalidade",
        back_populates="edital",
        cascade="all, delete-orphan",
    )
    vagas = relationship(
        "Vaga",
        back_populates="edital",
        cascade="all, delete-orphan",
        overlaps="modalidade,vagas",
    )
    anexos = relationship(
        "Anexo",
        back_populates="edital",
        cascade="all, delete-orphan",
        overlaps="vaga,anexos",
    )
    inscricoes = relationship(
        "Inscricao",
        back_populates="edital",
        cascade="all, delete-orphan",
        overlaps="vaga,inscricoes",
    )
    sync_logs = relationship(
        "SyncLog",
        back_populates="edital",
        cascade="all, delete-orphan",
    )
