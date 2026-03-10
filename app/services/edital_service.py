from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.database.connection import DatabaseConnection
from app.repositories.edital_repository import EditalRepository
from app.services.sync_service import SyncResult, SyncService


@dataclass(frozen=True)
class EditalSummary:
    id: int
    codigo: str
    titulo: str
    tipo_documento: str
    situacao: str | None
    modalidades_count: int
    vagas_count: int
    anexos_count: int
    synced_at: datetime | None


class EditalService:
    def __init__(self, database: DatabaseConnection, sync_service: SyncService):
        self.database = database
        self.sync_service = sync_service

    def list_editais(self) -> list[EditalSummary]:
        with self.database.session() as session:
            repository = EditalRepository(session)
            return [
                EditalSummary(
                    id=edital.id,
                    codigo=edital.codigo,
                    titulo=edital.titulo,
                    tipo_documento=edital.tipo_documento,
                    situacao=edital.situacao,
                    modalidades_count=edital.modalidades_count,
                    vagas_count=edital.vagas_count,
                    anexos_count=edital.anexos_count,
                    synced_at=edital.synced_at,
                )
                for edital in repository.list_all()
            ]

    def sync_edital(self, codigo: str, tipo_documento: str) -> SyncResult:
        return self.sync_service.sync_edital(codigo, tipo_documento)
