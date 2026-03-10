from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import customtkinter as ctk

from app.core.config import Config
from app.database.connection import DatabaseConnection
from app.services.api_client import ApiClient
from app.services.edital_service import EditalService
from app.services.sync_service import SyncService
from app.ui.main_window import MainWindow


def main() -> None:
    config = Config.from_env()
    database = DatabaseConnection(config)
    database.initialize()

    api_client = ApiClient(config)
    sync_service = SyncService(database, api_client)
    edital_service = EditalService(database, sync_service)

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = MainWindow(config=config, edital_service=edital_service)
    app.mainloop()


if __name__ == "__main__":
    main()
