from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker
from synapsecord_core.db.session import SessionLocal
from synapsecord_core.domain import (
    GameAccount,
    PlayerProfile,
    SynapseUser,
)

from synapsecord_bot.domains.registry import DomainRegistry
from synapsecord_bot.domains import DomainResolutionService
from synapsecord_bot.domains.resolvers import (
    GameAccountResolver,
    PlayerProfileResolver,
    SynapseUserResolver,
)
from synapsecord_bot.services.scope import ApplicationScope


class ServiceContainer:
    def __init__(
            self,
            session_factory: sessionmaker[Session] = SessionLocal
    ):
        self._session_factory = session_factory

        self.domain_registry = DomainRegistry()
        self.domain_registry.register(SynapseUser, SynapseUserResolver())
        self.domain_registry.register(GameAccount, GameAccountResolver())
        self.domain_registry.register(PlayerProfile, PlayerProfileResolver())

        self.domain_resolution = DomainResolutionService(self.domain_registry)

    def create_scope(self) -> ApplicationScope:
        return ApplicationScope(self._session_factory)