from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sync_log import SyncLog


class SyncLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, sync_log: SyncLog) -> SyncLog:
        self.session.add(sync_log)
        self.session.flush()
        return sync_log

    def list_recent(self, limit: int = 20) -> list[SyncLog]:
        statement = select(SyncLog).order_by(SyncLog.started_at.desc()).limit(limit)
        return self.session.scalars(statement).all()
