from __future__ import annotations

from sqlalchemy.orm import sessionmaker, Session

from synapsecord_bot.domains import DomainContext


class ApplicationScope:
    def __init__(self, session_factory: sessionmaker[Session]):
        self.domains = DomainContext()
        self._session_factory = session_factory
        self._session = None

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = self._session_factory()

        return self._session

    def close(self) -> None:
        if self._session is None:
            return

        self._session.close()
        self._session = None

    def __enter__(self) -> ApplicationScope:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
