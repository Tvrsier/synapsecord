from __future__ import annotations

from typing import Protocol, TypeVar

from synapsecord_bot.domains import DomainContext

TDomain = TypeVar("TDomain")


class DomainResolverContext(Protocol):
    @property
    def domains(self) -> DomainContext:
        ...


# noinspection variance
class DomainResolver(Protocol[TDomain]):
    async def resolve(self, ctx: DomainResolverContext) -> TDomain | None:
        ...