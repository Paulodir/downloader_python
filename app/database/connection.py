from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Config
from app.models import register_models


class DatabaseConnection:
    def __init__(self, config: Config):
        self.config = config
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(
            self.config.database_url,
            connect_args={"check_same_thread": False},
            future=True,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )

    def initialize(self) -> None:
        register_models()
        from app.database.schema import Base

        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        db_session = self.session_factory()
        try:
            yield db_session
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()
