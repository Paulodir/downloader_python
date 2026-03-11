from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.schema import Base, TimestampMixin


class Categoria(TimestampMixin, Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(Text(), nullable=False)
    versao: Mapped[int] = mapped_column(Integer(), nullable=False, default=1)
    status: Mapped[int] = mapped_column(Integer(), nullable=False, default=1)

    grupos = relationship(
        "Grupo",
        back_populates="categoria",
        cascade="all, delete-orphan",
    )
    anexos = relationship("Anexo", back_populates="categoria")
    sync_logs = relationship("SyncLog", back_populates="categoria")

    @property
    def descricao_exibicao(self) -> str:
        suffix = " (Versao Antiga)" if self.versao == 0 else ""
        return f"{self.descricao}{suffix}"

    @property
    def ativa(self) -> bool:
        return self.status == 1
