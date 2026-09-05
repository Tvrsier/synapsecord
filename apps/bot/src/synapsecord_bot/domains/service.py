from __future__ import annotations

from typing import TypeVar

from synapsecord_bot.domains import DomainRegistry, DomainResolverContext
from synapsecord_bot.domains.errors import CircularDomainResolutionError

TDomain =   TypeVar("TDomain")


class DomainResolutionService:
    def __init__(self, registry: DomainRegistry):
        self._registry = registry

    async def resolve(
            self,
            ctx: DomainResolverContext,
            domain_type: type[TDomain]
    ) -> TDomain | None:
        existing = ctx.domains.get(domain_type)
        if existing is not None:
            return existing

        if ctx.domains.is_resolving(domain_type):
            raise CircularDomainResolutionError(domain_type)

        resolver = self._registry.require(domain_type)

        ctx.domains.mark_resolving(domain_type)

        try:
            domain = await resolver.resolve(ctx)
        finally:
            ctx.domains.unmark_resolving(domain_type)

        if domain is not None:
            ctx.domains.set(domain)

        return domain
