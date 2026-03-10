from app.models.anexo import Anexo
from app.models.categoria import Categoria
from app.models.edital import Edital
from app.models.inscricao import Inscricao
from app.models.modalidade import Modalidade
from app.models.sync_log import SyncLog
from app.models.vaga import Vaga


def register_models() -> None:
    """Import side effect helper for metadata registration."""


__all__ = [
    "Anexo",
    "Categoria",
    "Edital",
    "Inscricao",
    "Modalidade",
    "SyncLog",
    "Vaga",
    "register_models",
]
