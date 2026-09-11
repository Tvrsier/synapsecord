from __future__ import annotations

from typing import TYPE_CHECKING

from synapsecord_bot.domains import DomainContext
from synapsecord_core.domain import SynapseUser, GameAccount, PlayerProfile

if TYPE_CHECKING:
    from synapsecord_bot.bot.bot import SynapseCORDBot
    from synapsecord_bot.services import ApplicationScope
    from synapsecord_bot.services.container import ServiceContainer
    import discord

class SynapseContextMixin:
    bot: SynapseCORDBot
    _scope: ApplicationScope
    author: discord.User | discord.Member

    def _initialize_synapse_context(self) -> None:
        self._scope = self.services.create_scope()

    @property
    def services(self) -> ServiceContainer:
        return self.bot.services

    @property
    def scope(self) -> ApplicationScope:
        return self._scope

    @property
    def domains(self) -> DomainContext:
        return self._scope.domains

    @property
    def synapse_user(self) -> SynapseUser:
        return self.domains.require(SynapseUser)

    @property
    def game_account(self) -> GameAccount:
        return self.domains.require(GameAccount)

    @property
    def player_profile(self) -> PlayerProfile:
        return self.domains.require(PlayerProfile)

    @property
    def discord_user_id(self) -> int:
        return self.author.id

    def close_scope(self) -> None:
        self._scope.close()