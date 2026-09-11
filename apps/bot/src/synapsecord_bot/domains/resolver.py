from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from synapsecord_bot.domains.context import DomainContext

if TYPE_CHECKING:
    from synapsecord_bot.services.container import ServiceContainer
    from synapsecord_bot.services.scope import ApplicationScope

TDomain = TypeVar("TDomain")


class DomainResolverContext(Protocol):
    @property
    def domains(self) -> DomainContext:
        ...

    @property
    def scope(self) -> ApplicationScope:
        ...

    @property
    def discord_user_id(self) -> int:
        ...

    @property
    def services(self) -> ServiceContainer:
        ...


# noinspection variance
class DomainResolver(Protocol[TDomain]):
    async def resolve(self, ctx: DomainResolverContext) -> TDomain | None:
        ...