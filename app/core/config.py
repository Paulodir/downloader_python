from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    app_name: str
    data_dir: Path
    database_path: Path
    api_base_url: str
    api_edital_path: str
    request_timeout: float
    document_types: tuple[str, ...]

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path.as_posix()}"

    @classmethod
    def from_env(cls) -> "Config":
        project_root = Path(__file__).resolve().parents[2]
        data_dir = project_root / "data"

        document_types = tuple(
            item.strip()
            for item in os.getenv(
                "APP_DOCUMENT_TYPES",
                "EDITAL,RESULTADO,RETIFICACAO,COMUNICADO",
            ).split(",")
            if item.strip()
        )

        return cls(
            app_name=os.getenv("APP_NAME", "Editais Desktop"),
            data_dir=data_dir,
            database_path=data_dir / os.getenv("APP_DATABASE_NAME", "editais.sqlite3"),
            api_base_url=os.getenv("APP_API_BASE_URL", "").rstrip("/"),
            api_edital_path=os.getenv("APP_API_EDITAL_PATH", "/editais/{codigo}"),
            request_timeout=float(os.getenv("APP_REQUEST_TIMEOUT", "30")),
            document_types=document_types or ("EDITAL",),
        )
