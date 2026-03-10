from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import select

from app.core.exceptions import SyncError, ValidationError
from app.database.connection import DatabaseConnection
from app.models import (
    Anexo,
    Categoria,
    Documento,
    Edital,
    Grupo,
    Inscricao,
    Modalidade,
    Subgrupo,
    SyncLog,
    Vaga,
)
from app.repositories import (
    AnexoRepository,
    DocumentoRepository,
    EditalRepository,
    InscricaoRepository,
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
            inscricao_repository = InscricaoRepository(session)
            anexo_repository = AnexoRepository(session)
            documento_repository = DocumentoRepository(session)
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
                documento_repository.delete_by_edital_id(edital.id)
                anexo_repository.delete_by_edital_id(edital.id)
                inscricao_repository.delete_by_edital_id(edital.id)
                vaga_repository.delete_by_edital_id(edital.id)
                modalidade_repository.delete_by_edital_id(edital.id)

                categoria_cache: dict[str, Categoria] = {}
                grupo_cache: dict[tuple[int, str], Grupo] = {}
                subgrupo_cache: dict[tuple[int, str], Subgrupo] = {}

                modalidades_total = 0
                vagas_total = 0
                inscricoes_total = 0
                anexos_total = 0
                documentos_total = 0
                modalidade_code_to_id: dict[str, int] = {}

                for categoria_payload in normalized["categorias"]:
                    self._sync_taxonomy_payload(
                        session=session,
                        payload=categoria_payload,
                        vaga_id=None,
                        categoria_cache=categoria_cache,
                        grupo_cache=grupo_cache,
                        subgrupo_cache=subgrupo_cache,
                    )

                for modalidade_payload in normalized["modalidades"]:
                    modalidade = Modalidade(
                        edital_id=edital.id,
                        codigo=self._pick_first(modalidade_payload, "codigo", "id", "codigoModalidade"),
                        nome=self._extract_name(modalidade_payload, default="Modalidade sem nome"),
                        descricao=self._pick_first(modalidade_payload, "descricao", "resumo"),
                        raw_payload=modalidade_payload,
                    )
                    modalidade_repository.save(modalidade)
                    modalidades_total += 1
                    if modalidade.codigo:
                        modalidade_code_to_id[str(modalidade.codigo)] = modalidade.id

                    for vaga_payload in self._extract_vagas(modalidade_payload):
                        vaga, vaga_inscricoes, vaga_anexos, vaga_documentos = self._sync_vaga(
                            session=session,
                            edital_id=edital.id,
                            modalidade_id=modalidade.id,
                            payload=vaga_payload,
                            categoria_cache=categoria_cache,
                            grupo_cache=grupo_cache,
                            subgrupo_cache=subgrupo_cache,
                            vaga_repository=vaga_repository,
                            inscricao_repository=inscricao_repository,
                            anexo_repository=anexo_repository,
                            documento_repository=documento_repository,
                        )
                        vagas_total += 1
                        inscricoes_total += vaga_inscricoes
                        anexos_total += vaga_anexos
                        documentos_total += vaga_documentos

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

                    vaga, vaga_inscricoes, vaga_anexos, vaga_documentos = self._sync_vaga(
                        session=session,
                        edital_id=edital.id,
                        modalidade_id=modalidade_id,
                        payload=vaga_payload,
                        categoria_cache=categoria_cache,
                        grupo_cache=grupo_cache,
                        subgrupo_cache=subgrupo_cache,
                        vaga_repository=vaga_repository,
                        inscricao_repository=inscricao_repository,
                        anexo_repository=anexo_repository,
                        documento_repository=documento_repository,
                    )
                    vagas_total += 1
                    inscricoes_total += vaga_inscricoes
                    anexos_total += vaga_anexos
                    documentos_total += vaga_documentos

                root_anexos, root_documentos = self._save_anexos_for_owner(
                    session=session,
                    anexo_repository=anexo_repository,
                    documento_repository=documento_repository,
                    edital_id=edital.id,
                    vaga_id=None,
                    inscricao_id=None,
                    payload=normalized["root_payload"],
                    default_vaga_id=None,
                    categoria_cache=categoria_cache,
                    grupo_cache=grupo_cache,
                    subgrupo_cache=subgrupo_cache,
                )
                anexos_total += root_anexos
                documentos_total += root_documentos

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
                    "inscricoes": inscricoes_total,
                    "anexos": anexos_total,
                    "documentos": documentos_total,
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

    def _sync_vaga(
        self,
        session,
        edital_id: int,
        modalidade_id: int | None,
        payload: dict[str, Any],
        categoria_cache: dict[str, Categoria],
        grupo_cache: dict[tuple[int, str], Grupo],
        subgrupo_cache: dict[tuple[int, str], Subgrupo],
        vaga_repository: VagaRepository,
        inscricao_repository: InscricaoRepository,
        anexo_repository: AnexoRepository,
        documento_repository: DocumentoRepository,
    ) -> tuple[Vaga, int, int, int]:
        vaga = self._build_vaga(
            edital_id=edital_id,
            modalidade_id=modalidade_id,
            payload=payload,
        )
        vaga_repository.save(vaga)

        self._seed_taxonomies_from_payload(
            session=session,
            payload=payload,
            vaga_id=vaga.id,
            categoria_cache=categoria_cache,
            grupo_cache=grupo_cache,
            subgrupo_cache=subgrupo_cache,
        )

        inscricoes_total = 0
        anexos_total = 0
        documentos_total = 0

        for inscricao_payload in self._extract_inscricoes(payload):
            inscricao = self._build_inscricao(
                edital_id=edital_id,
                vaga_id=vaga.id,
                payload=inscricao_payload,
            )
            inscricao_repository.save(inscricao)
            inscricoes_total += 1

            self._seed_taxonomies_from_payload(
                session=session,
                payload=inscricao_payload,
                vaga_id=vaga.id,
                categoria_cache=categoria_cache,
                grupo_cache=grupo_cache,
                subgrupo_cache=subgrupo_cache,
            )

            inscricao_anexos, inscricao_documentos = self._save_anexos_for_owner(
                session=session,
                anexo_repository=anexo_repository,
                documento_repository=documento_repository,
                edital_id=edital_id,
                vaga_id=vaga.id,
                inscricao_id=inscricao.id,
                payload=inscricao_payload,
                default_vaga_id=vaga.id,
                categoria_cache=categoria_cache,
                grupo_cache=grupo_cache,
                subgrupo_cache=subgrupo_cache,
            )
            anexos_total += inscricao_anexos
            documentos_total += inscricao_documentos

        vaga_anexos, vaga_documentos = self._save_anexos_for_owner(
            session=session,
            anexo_repository=anexo_repository,
            documento_repository=documento_repository,
            edital_id=edital_id,
            vaga_id=vaga.id,
            inscricao_id=None,
            payload=payload,
            default_vaga_id=vaga.id,
            categoria_cache=categoria_cache,
            grupo_cache=grupo_cache,
            subgrupo_cache=subgrupo_cache,
        )
        anexos_total += vaga_anexos
        documentos_total += vaga_documentos

        return vaga, inscricoes_total, anexos_total, documentos_total

    def _save_anexos_for_owner(
        self,
        session,
        anexo_repository: AnexoRepository,
        documento_repository: DocumentoRepository,
        edital_id: int,
        vaga_id: int | None,
        inscricao_id: int | None,
        payload: dict[str, Any],
        default_vaga_id: int | None,
        categoria_cache: dict[str, Categoria],
        grupo_cache: dict[tuple[int, str], Grupo],
        subgrupo_cache: dict[tuple[int, str], Subgrupo],
    ) -> tuple[int, int]:
        anexos_total = 0
        documentos_total = 0

        for anexo_payload in self._extract_anexos(payload):
            categoria, _, subgrupo = self._resolve_taxonomy_context(
                session=session,
                payload=anexo_payload,
                vaga_id=default_vaga_id,
                categoria_cache=categoria_cache,
                grupo_cache=grupo_cache,
                subgrupo_cache=subgrupo_cache,
            )

            anexo = self._build_anexo(
                edital_id=edital_id,
                vaga_id=vaga_id,
                inscricao_id=inscricao_id,
                categoria_id=categoria.id if categoria else None,
                subgrupo_id=subgrupo.id if subgrupo else None,
                payload=anexo_payload,
            )
            anexo_repository.save(anexo)
            anexos_total += 1

            for documento_payload in self._extract_documentos(anexo_payload):
                documento = self._build_documento(anexo.id, documento_payload)
                documento_repository.save(documento)
                documentos_total += 1

        return anexos_total, documentos_total

    def _seed_taxonomies_from_payload(
        self,
        session,
        payload: dict[str, Any],
        vaga_id: int | None,
        categoria_cache: dict[str, Categoria],
        grupo_cache: dict[tuple[int, str], Grupo],
        subgrupo_cache: dict[tuple[int, str], Subgrupo],
    ) -> None:
        for categoria_payload in self._extract_collection(payload, payload, "categorias", "categories"):
            self._sync_taxonomy_payload(
                session=session,
                payload=categoria_payload,
                vaga_id=vaga_id,
                categoria_cache=categoria_cache,
                grupo_cache=grupo_cache,
                subgrupo_cache=subgrupo_cache,
            )

    def _sync_taxonomy_payload(
        self,
        session,
        payload: dict[str, Any],
        vaga_id: int | None,
        categoria_cache: dict[str, Categoria],
        grupo_cache: dict[tuple[int, str], Grupo],
        subgrupo_cache: dict[tuple[int, str], Subgrupo],
    ) -> tuple[Categoria | None, Grupo | None, Subgrupo | None]:
        categoria, grupo, subgrupo = self._resolve_taxonomy_context(
            session=session,
            payload=payload,
            vaga_id=vaga_id,
            categoria_cache=categoria_cache,
            grupo_cache=grupo_cache,
            subgrupo_cache=subgrupo_cache,
        )

        for grupo_payload in self._extract_collection(payload, payload, "grupos", "groups"):
            grupo_nome = self._extract_name(grupo_payload)
            if not categoria or not grupo_nome:
                continue

            grupo = self._get_or_create_grupo(
                session=session,
                categoria=categoria,
                nome=grupo_nome,
                descricao=self._pick_first(grupo_payload or {}, "descricao", "resumo"),
                payload=grupo_payload,
                grupo_cache=grupo_cache,
            )
            for subgrupo_payload in self._extract_collection(grupo_payload, grupo_payload, "subgrupos", "subgroups"):
                subgrupo_nome = self._extract_name(subgrupo_payload)
                if not subgrupo_nome:
                    continue
                self._get_or_create_subgrupo(
                    session=session,
                    grupo=grupo,
                    nome=subgrupo_nome,
                    descricao=self._pick_first(subgrupo_payload, "descricao", "resumo"),
                    payload=subgrupo_payload,
                    subgrupo_cache=subgrupo_cache,
                )

        return categoria, grupo, subgrupo

    def _resolve_taxonomy_context(
        self,
        session,
        payload: dict[str, Any],
        vaga_id: int | None,
        categoria_cache: dict[str, Categoria],
        grupo_cache: dict[tuple[int, str], Grupo],
        subgrupo_cache: dict[tuple[int, str], Subgrupo],
    ) -> tuple[Categoria | None, Grupo | None, Subgrupo | None]:
        categoria_payload = payload.get("categoria") if isinstance(payload.get("categoria"), dict) else payload
        categoria_nome = self._extract_name_from_payload(
            payload,
            dict_keys=("categoria_nome", "categoriaNome"),
            nested_key="categoria",
        )
        if not categoria_nome and isinstance(categoria_payload, dict):
            categoria_nome = self._extract_name(categoria_payload)
        categoria = None
        if categoria_nome:
            categoria = self._get_or_create_categoria(
                session=session,
                nome=categoria_nome,
                descricao=self._pick_first(categoria_payload, "descricao", "resumo"),
                payload=categoria_payload if isinstance(categoria_payload, dict) else payload,
                vaga_id=vaga_id,
                categoria_cache=categoria_cache,
            )

        grupo = None
        grupo_payload = payload.get("grupo") if isinstance(payload.get("grupo"), dict) else None
        grupo_nome = self._extract_name_from_payload(
            payload,
            dict_keys=("grupo_nome", "grupoNome"),
            nested_key="grupo",
        )
        if not grupo_nome and isinstance(grupo_payload, dict):
            grupo_nome = self._extract_name(grupo_payload)
        if categoria and grupo_nome:
            grupo = self._get_or_create_grupo(
                session=session,
                categoria=categoria,
                nome=grupo_nome,
                descricao=self._pick_first(grupo_payload, "descricao", "resumo"),
                payload=grupo_payload,
                grupo_cache=grupo_cache,
            )

        subgrupo = None
        subgrupo_payload = payload.get("subgrupo") if isinstance(payload.get("subgrupo"), dict) else None
        subgrupo_nome = self._extract_name_from_payload(
            payload,
            dict_keys=("subgrupo_nome", "subgrupoNome"),
            nested_key="subgrupo",
        )
        if not subgrupo_nome and isinstance(subgrupo_payload, dict):
            subgrupo_nome = self._extract_name(subgrupo_payload)
        if grupo and subgrupo_nome:
            subgrupo = self._get_or_create_subgrupo(
                session=session,
                grupo=grupo,
                nome=subgrupo_nome,
                descricao=self._pick_first(subgrupo_payload or {}, "descricao", "resumo"),
                payload=subgrupo_payload,
                subgrupo_cache=subgrupo_cache,
            )

        return categoria, grupo, subgrupo

    def _get_or_create_categoria(
        self,
        session,
        nome: str,
        descricao: str | None,
        payload: dict[str, Any],
        vaga_id: int | None,
        categoria_cache: dict[str, Categoria],
    ) -> Categoria:
        key = nome.strip().lower()
        if key in categoria_cache:
            categoria = categoria_cache[key]
            if vaga_id and categoria.vaga_id is None:
                categoria.vaga_id = vaga_id
            return categoria

        categoria = session.scalar(select(Categoria).where(Categoria.nome == nome))
        if categoria is None:
            categoria = Categoria(
                nome=nome,
                descricao=descricao,
                vaga_id=vaga_id,
                raw_payload=payload,
            )
            session.add(categoria)
            session.flush()
        else:
            if descricao and not categoria.descricao:
                categoria.descricao = descricao
            if vaga_id and categoria.vaga_id is None:
                categoria.vaga_id = vaga_id
            if payload and categoria.raw_payload is None:
                categoria.raw_payload = payload

        categoria_cache[key] = categoria
        return categoria

    def _get_or_create_grupo(
        self,
        session,
        categoria: Categoria,
        nome: str,
        descricao: str | None,
        payload: dict[str, Any],
        grupo_cache: dict[tuple[int, str], Grupo],
    ) -> Grupo:
        key = (categoria.id, nome.strip().lower())
        if key in grupo_cache:
            return grupo_cache[key]

        grupo = session.scalar(
            select(Grupo).where(
                Grupo.categoria_id == categoria.id,
                Grupo.nome == nome,
            )
        )
        if grupo is None:
            grupo = Grupo(
                categoria_id=categoria.id,
                nome=nome,
                descricao=descricao,
                raw_payload=payload,
            )
            session.add(grupo)
            session.flush()
        else:
            if descricao and not grupo.descricao:
                grupo.descricao = descricao
            if payload and grupo.raw_payload is None:
                grupo.raw_payload = payload

        grupo_cache[key] = grupo
        return grupo

    def _get_or_create_subgrupo(
        self,
        session,
        grupo: Grupo,
        nome: str,
        descricao: str | None,
        payload: dict[str, Any],
        subgrupo_cache: dict[tuple[int, str], Subgrupo],
    ) -> Subgrupo:
        key = (grupo.id, nome.strip().lower())
        if key in subgrupo_cache:
            return subgrupo_cache[key]

        subgrupo = session.scalar(
            select(Subgrupo).where(
                Subgrupo.grupo_id == grupo.id,
                Subgrupo.nome == nome,
            )
        )
        if subgrupo is None:
            subgrupo = Subgrupo(
                grupo_id=grupo.id,
                nome=nome,
                descricao=descricao,
                raw_payload=payload,
            )
            session.add(subgrupo)
            session.flush()
        else:
            if descricao and not subgrupo.descricao:
                subgrupo.descricao = descricao
            if payload and subgrupo.raw_payload is None:
                subgrupo.raw_payload = payload

        subgrupo_cache[key] = subgrupo
        return subgrupo

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

        return {
            "codigo": codigo,
            "tipo_documento": tipo_documento,
            "titulo": str(titulo).strip() or f"Edital {codigo}",
            "descricao": self._pick_first(root, "descricao", "resumo", "ementa"),
            "situacao": self._pick_first(root, "situacao", "status"),
            "root_payload": root,
            "modalidades": self._extract_collection(root, payload, "modalidades", "modalities", "cursos"),
            "vagas": self._extract_collection(root, payload, "vagas", "vacancies", "oportunidades"),
            "anexos": self._extract_collection(root, payload, "anexos", "documentos", "attachments"),
            "categorias": self._extract_collection(root, payload, "categorias", "categories"),
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
        return self._extract_collection(modalidade_payload, modalidade_payload, "vagas", "vacancies", "oportunidades")

    def _extract_inscricoes(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return self._extract_collection(
            payload,
            payload,
            "inscricoes",
            "inscriptions",
            "registrations",
        )

    def _extract_anexos(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return self._extract_collection(payload, payload, "anexos", "documentos", "attachments")

    def _extract_documentos(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return self._extract_collection(
            payload,
            payload,
            "documentos",
            "docs",
            "arquivos",
            "files",
        )

    def _build_vaga(self, edital_id: int, modalidade_id: int | None, payload: dict[str, Any]) -> Vaga:
        quantidade = self._pick_first(payload, "quantidade", "qtd", "total")
        return Vaga(
            edital_id=edital_id,
            modalidade_id=modalidade_id,
            codigo=self._pick_first(payload, "codigo", "id", "codigoVaga"),
            titulo=self._extract_name(payload, default="Vaga sem titulo"),
            descricao=self._pick_first(payload, "descricao", "resumo"),
            quantidade=self._coerce_int(quantidade),
            turno=self._pick_first(payload, "turno", "periodo"),
            local=self._pick_first(payload, "local", "campus", "cidade"),
            raw_payload=payload,
        )

    def _build_inscricao(self, edital_id: int, vaga_id: int, payload: dict[str, Any]) -> Inscricao:
        return Inscricao(
            edital_id=edital_id,
            vaga_id=vaga_id,
            status=self._pick_first(payload, "status", "situacao", default="pendente"),
            inicio=self._coerce_datetime(self._pick_first(payload, "inicio", "data_inicio", "dataInicio")),
            fim=self._coerce_datetime(self._pick_first(payload, "fim", "data_fim", "dataFim")),
            raw_payload=payload,
        )

    def _build_anexo(
        self,
        edital_id: int,
        vaga_id: int | None,
        inscricao_id: int | None,
        categoria_id: int | None,
        subgrupo_id: int | None,
        payload: dict[str, Any],
    ) -> Anexo:
        return Anexo(
            edital_id=edital_id,
            vaga_id=vaga_id,
            inscricao_id=inscricao_id,
            categoria_id=categoria_id,
            subgrupo_id=subgrupo_id,
            codigo=self._pick_first(payload, "codigo", "id", "codigoAnexo"),
            nome=self._extract_name(payload, default="Documento"),
            tipo_documento=self._pick_first(payload, "tipo_documento", "tipoDocumento", "tipo"),
            extensao=self._pick_first(payload, "extensao", "extension"),
            url=self._pick_first(payload, "url", "link", "download_url", "downloadUrl"),
            raw_payload=payload,
        )

    def _build_documento(self, anexo_id: int, payload: dict[str, Any]) -> Documento:
        return Documento(
            anexo_id=anexo_id,
            nome=self._extract_name(payload, default="Arquivo"),
            descricao=self._pick_first(payload, "descricao", "resumo"),
            url=self._pick_first(payload, "url", "link", "download_url", "downloadUrl"),
            raw_payload=payload,
        )

    def _extract_name_from_payload(
        self,
        payload: dict[str, Any],
        dict_keys: tuple[str, ...],
        nested_key: str,
    ) -> str | None:
        nested = payload.get(nested_key)
        if isinstance(nested, dict):
            name = self._extract_name(nested)
            if name:
                return name
        direct = self._pick_first(payload, *dict_keys)
        if isinstance(direct, str) and direct.strip():
            return direct.strip()
        if isinstance(direct, dict):
            return self._extract_name(direct)
        return None

    def _extract_name(self, payload: dict[str, Any], default: str | None = None) -> str | None:
        value = self._pick_first(
            payload,
            "nome",
            "titulo",
            "descricao",
            "label",
            "value",
        )
        if value in (None, ""):
            return default
        return str(value).strip() or default

    def _pick_first(self, payload: dict[str, Any], *keys: str, default: Any = None) -> Any:
        if not isinstance(payload, dict):
            return default
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

    def _coerce_datetime(self, value: Any) -> datetime | None:
        if value in (None, ""):
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            normalized = value.strip().replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(normalized)
            except ValueError:
                return None
        return None
