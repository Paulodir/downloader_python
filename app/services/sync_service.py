from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.core.exceptions import SyncError, ValidationError
from app.database.connection import DatabaseConnection
from app.models import Anexo, Edital, Modalidade, SyncLog, Vaga
from app.repositories import (
    AnexoRepository,
    EditalRepository,
    ModalidadeRepository,
    SyncLogRepository,
    VagaRepository,
)
from app.services.api_client import ApiClient


@dataclass(frozen=True)
class SyncResult:
    edital_id: int
    codigo: str
    titulo: str
    tipo_documento: str
    modalidades: int
    vagas: int
    anexos: int
    synced_at: datetime


class SyncService:
    def __init__(self, database: DatabaseConnection, api_client: ApiClient):
        self.database = database
        self.api_client = api_client

    def sync_edital(self, codigo: str, tipo_documento: str) -> SyncResult:
        codigo_normalizado = codigo.strip()
        tipo_documento_normalizado = tipo_documento.strip()
        if not codigo_normalizado:
            raise ValidationError("Informe o codigo do edital.")
        if not tipo_documento_normalizado:
            raise ValidationError("Informe o tipo de documento.")

        payload = self.api_client.fetch_edital(codigo_normalizado, tipo_documento_normalizado)
        normalized = self._normalize_payload(payload, codigo_normalizado, tipo_documento_normalizado)
        now = datetime.utcnow()

        with self.database.session() as session:
            edital_repository = EditalRepository(session)
            modalidade_repository = ModalidadeRepository(session)
            vaga_repository = VagaRepository(session)
            anexo_repository = AnexoRepository(session)
            sync_log_repository = SyncLogRepository(session)

            edital = edital_repository.get_by_codigo(codigo_normalizado)
            if edital is None:
                edital = Edital(
                    codigo=codigo_normalizado,
                    titulo=normalized["titulo"],
                    tipo_documento=tipo_documento_normalizado,
                )

            edital.titulo = normalized["titulo"]
            edital.descricao = normalized["descricao"]
            edital.situacao = normalized["situacao"]
            edital.tipo_documento = tipo_documento_normalizado
            edital.synced_at = now
            edital.raw_payload = payload
            edital_repository.save(edital)

            sync_log = SyncLog(
                edital_id=edital.id,
                codigo_edital=codigo_normalizado,
                tipo_documento=tipo_documento_normalizado,
                status="started",
                started_at=now,
            )
            sync_log_repository.save(sync_log)

            try:
                anexo_repository.delete_by_edital_id(edital.id)
                vaga_repository.delete_by_edital_id(edital.id)
                modalidade_repository.delete_by_edital_id(edital.id)

                modalidades_total = 0
                vagas_total = 0
                anexos_total = 0
                modalidade_code_to_id: dict[str, int] = {}

                for modalidade_payload in normalized["modalidades"]:
                    modalidade = Modalidade(
                        edital_id=edital.id,
                        codigo=self._pick_first(modalidade_payload, "codigo", "id", "codigoModalidade"),
                        nome=self._pick_first(
                            modalidade_payload,
                            "nome",
                            "titulo",
                            "descricao",
                            default="Modalidade sem nome",
                        ),
                        descricao=self._pick_first(modalidade_payload, "descricao", "resumo"),
                        raw_payload=modalidade_payload,
                    )
                    modalidade_repository.save(modalidade)
                    modalidades_total += 1
                    if modalidade.codigo:
                        modalidade_code_to_id[str(modalidade.codigo)] = modalidade.id

                    for vaga_payload in self._extract_vagas(modalidade_payload):
                        vaga = self._build_vaga(
                            edital_id=edital.id,
                            modalidade_id=modalidade.id,
                            payload=vaga_payload,
                        )
                        vaga_repository.save(vaga)
                        vagas_total += 1
                        anexos_total += self._save_anexos_for_vaga(
                            anexo_repository=anexo_repository,
                            edital_id=edital.id,
                            vaga_id=vaga.id,
                            payload=vaga_payload,
                        )

                for vaga_payload in normalized["vagas"]:
                    modalidade_id = None
                    modalidade_codigo = self._pick_first(
                        vaga_payload,
                        "modalidade_codigo",
                        "modalidadeCodigo",
                        "codigoModalidade",
                    )
                    if modalidade_codigo is not None:
                        modalidade_id = modalidade_code_to_id.get(str(modalidade_codigo))

                    vaga = self._build_vaga(
                        edital_id=edital.id,
                        modalidade_id=modalidade_id,
                        payload=vaga_payload,
                    )
                    vaga_repository.save(vaga)
                    vagas_total += 1
                    anexos_total += self._save_anexos_for_vaga(
                        anexo_repository=anexo_repository,
                        edital_id=edital.id,
                        vaga_id=vaga.id,
                        payload=vaga_payload,
                    )

                for anexo_payload in normalized["anexos"]:
                    anexo = self._build_anexo(
                        edital_id=edital.id,
                        vaga_id=None,
                        payload=anexo_payload,
                    )
                    anexo_repository.save(anexo)
                    anexos_total += 1

                edital.modalidades_count = modalidades_total
                edital.vagas_count = vagas_total
                edital.anexos_count = anexos_total
                edital_repository.save(edital)

                sync_log.status = "success"
                sync_log.finished_at = datetime.utcnow()
                sync_log.message = "Sincronizacao concluida."
                sync_log.payload_summary = {
                    "modalidades": modalidades_total,
                    "vagas": vagas_total,
                    "anexos": anexos_total,
                }
                sync_log_repository.save(sync_log)
            except Exception as exc:
                sync_log.status = "error"
                sync_log.finished_at = datetime.utcnow()
                sync_log.message = str(exc)
                sync_log_repository.save(sync_log)
                if isinstance(exc, (ValidationError, SyncError)):
                    raise
                raise SyncError(f"Falha ao persistir o edital {codigo_normalizado}: {exc}") from exc

            return SyncResult(
                edital_id=edital.id,
                codigo=edital.codigo,
                titulo=edital.titulo,
                tipo_documento=edital.tipo_documento,
                modalidades=edital.modalidades_count,
                vagas=edital.vagas_count,
                anexos=edital.anexos_count,
                synced_at=edital.synced_at or now,
            )

    def _normalize_payload(
        self,
        payload: dict[str, Any],
        codigo: str,
        tipo_documento: str,
    ) -> dict[str, Any]:
        root = payload
        for key in ("data", "edital", "item", "resultado"):
            value = payload.get(key)
            if isinstance(value, dict):
                root = value
                break

        titulo = self._pick_first(
            root,
            "titulo",
            "nome",
            "descricao",
            "tituloEdital",
            default=f"Edital {codigo}",
        )

        modalidades = self._extract_collection(root, payload, "modalidades", "modalities", "cursos")
        vagas = self._extract_collection(root, payload, "vagas", "vacancies", "oportunidades")
        anexos = self._extract_collection(root, payload, "anexos", "documentos", "attachments")

        return {
            "codigo": codigo,
            "tipo_documento": tipo_documento,
            "titulo": str(titulo).strip() or f"Edital {codigo}",
            "descricao": self._pick_first(root, "descricao", "resumo", "ementa"),
            "situacao": self._pick_first(root, "situacao", "status"),
            "modalidades": modalidades,
            "vagas": vagas,
            "anexos": anexos,
        }

    def _extract_collection(
        self,
        primary: dict[str, Any],
        secondary: dict[str, Any],
        *keys: str,
    ) -> list[dict[str, Any]]:
        for source in (primary, secondary):
            for key in keys:
                value = source.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]
        return []

    def _extract_vagas(self, modalidade_payload: dict[str, Any]) -> list[dict[str, Any]]:
        for key in ("vagas", "vacancies", "oportunidades"):
            value = modalidade_payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return []

    def _save_anexos_for_vaga(
        self,
        anexo_repository: AnexoRepository,
        edital_id: int,
        vaga_id: int,
        payload: dict[str, Any],
    ) -> int:
        total = 0
        for anexo_payload in self._extract_collection(payload, payload, "anexos", "documentos", "attachments"):
            anexo = self._build_anexo(edital_id=edital_id, vaga_id=vaga_id, payload=anexo_payload)
            anexo_repository.save(anexo)
            total += 1
        return total

    def _build_vaga(self, edital_id: int, modalidade_id: int | None, payload: dict[str, Any]) -> Vaga:
        quantidade = self._pick_first(payload, "quantidade", "qtd", "total")
        return Vaga(
            edital_id=edital_id,
            modalidade_id=modalidade_id,
            codigo=self._pick_first(payload, "codigo", "id", "codigoVaga"),
            titulo=self._pick_first(
                payload,
                "titulo",
                "nome",
                "descricao",
                default="Vaga sem titulo",
            ),
            descricao=self._pick_first(payload, "descricao", "resumo"),
            quantidade=self._coerce_int(quantidade),
            turno=self._pick_first(payload, "turno", "periodo"),
            local=self._pick_first(payload, "local", "campus", "cidade"),
            raw_payload=payload,
        )

    def _build_anexo(self, edital_id: int, vaga_id: int | None, payload: dict[str, Any]) -> Anexo:
        nome = self._pick_first(payload, "nome", "titulo", "descricao", default="Documento")
        url = self._pick_first(payload, "url", "link", "download_url", "downloadUrl")
        return Anexo(
            edital_id=edital_id,
            vaga_id=vaga_id,
            codigo=self._pick_first(payload, "codigo", "id", "codigoAnexo"),
            nome=nome,
            tipo_documento=self._pick_first(payload, "tipo_documento", "tipoDocumento", "tipo"),
            extensao=self._pick_first(payload, "extensao", "extension"),
            url=url,
            raw_payload=payload,
        )

    def _pick_first(self, payload: dict[str, Any], *keys: str, default: Any = None) -> Any:
        for key in keys:
            value = payload.get(key)
            if value not in (None, ""):
                return value
        return default

    def _coerce_int(self, value: Any) -> int | None:
        if value in (None, ""):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
