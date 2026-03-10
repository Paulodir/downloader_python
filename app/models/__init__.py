from app.models.anexo import Anexo
from app.models.categoria import Categoria
from app.models.documento import Documento
from app.models.edital import Edital
from app.models.grupo import Grupo
from app.models.inscricao import Inscricao
from app.models.modalidade import Modalidade
from app.models.subgrupo import Subgrupo
from app.models.sync_log import SyncLog
from app.models.vaga import Vaga


def register_models() -> None:
    """Import side effect helper for metadata registration."""


__all__ = [
    "Anexo",
    "Categoria",
    "Documento",
    "Edital",
    "Grupo",
    "Inscricao",
    "Modalidade",
    "Subgrupo",
    "SyncLog",
    "Vaga",
    "register_models",
]
