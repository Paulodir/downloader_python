from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoriaSeedRecord:
    id: int
    descricao: str
    versao: int
    status: int


class CategoriaSeedData:
    DEFAULT_RECORDS: tuple[CategoriaSeedRecord, ...] = (
        CategoriaSeedRecord(1, "Requisicao de Documentos", 0, 1),
        CategoriaSeedRecord(2, "Pedidos", 0, 1),
        CategoriaSeedRecord(3, "Titulos", 0, 1),
        CategoriaSeedRecord(4, "Uploads do Edital", 1, 1),
        CategoriaSeedRecord(5, "Uploads do Candidato", 1, 1),
        CategoriaSeedRecord(6, "Isencoes", 1, 1),
        CategoriaSeedRecord(7, "Condicoes Especiais", 1, 1),
        CategoriaSeedRecord(8, "Solicitacoes", 1, 1),
        CategoriaSeedRecord(9, "Titulos", 1, 1),
        CategoriaSeedRecord(10, "Foto do Candidato", 1, 1),
        CategoriaSeedRecord(11, "Comprovantes", 1, 0),
    )
