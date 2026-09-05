from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker
from synapsecord_core.db.session import SessionLocal


class ServiceContainer:
    def __init__(
            self,
            session_factory: sessionmaker[Session] = SessionLocal
    ):
        self.session_factory = session_factory