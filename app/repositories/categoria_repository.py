from __future__ import annotations

import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.category_seed import CategoriaSeedRecord
from app.models.categoria import Categoria


class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Categoria]:
        statement = select(Categoria).order_by(Categoria.id.asc())
        return self.session.scalars(statement).all()

    def list_active(self) -> list[Categoria]:
        statement = select(Categoria).where(Categoria.status == 1).order_by(Categoria.id.asc())
        return self.session.scalars(statement).all()

    def get_by_id(self, categoria_id: int) -> Categoria | None:
        return self.session.get(Categoria, categoria_id)

    def get_by_descricao(self, descricao: str, only_active: bool = False) -> Categoria | None:
        normalized_target = self._normalize_text(descricao)
        candidates = self.list_active() if only_active else self.list_all()
        for categoria in candidates:
            if self._normalize_text(categoria.descricao) == normalized_target:
                return categoria
        return None

    def ensure_defaults(self, records: list[CategoriaSeedRecord] | tuple[CategoriaSeedRecord, ...]) -> int:
        existing_by_id = {categoria.id: categoria for categoria in self.list_all()}
        changed = 0

        for record in records:
            categoria_id = record.id
            descricao = record.descricao.strip()
            versao = record.versao
            status = record.status

            categoria = existing_by_id.get(categoria_id)
            if categoria is None:
                categoria = Categoria(
                    id=categoria_id,
                    descricao=descricao,
                    versao=versao,
                    status=status,
                )
                self.session.add(categoria)
                changed += 1
                continue

            updated = False
            if categoria.descricao != descricao:
                categoria.descricao = descricao
                updated = True
            if categoria.versao != versao:
                categoria.versao = versao
                updated = True
            if categoria.status != status:
                categoria.status = status
                updated = True
            if updated:
                changed += 1

        self.session.flush()
        return changed

    def _normalize_text(self, value: str | None) -> str:
        normalized = unicodedata.normalize("NFKD", value or "")
        return "".join(ch for ch in normalized if not unicodedata.combining(ch)).strip().casefold()
