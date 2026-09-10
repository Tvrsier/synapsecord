from __future__ import annotations

from typing import TYPE_CHECKING

from synapsecord_bot.domains import DomainContext

if TYPE_CHECKING:
    from synapsecord_bot.bot.bot import SynapseCORDBot
    from synapsecord_bot.services.container import ServiceContainer

class SynapseContextMixin:
    bot: SynapseCORDBot
    domains: DomainContext

    def _initialize_synapse_context(self) -> None:
        self.domains = DomainContext()

    @property
    def services(self) -> ServiceContainer:
        return self.bot.services