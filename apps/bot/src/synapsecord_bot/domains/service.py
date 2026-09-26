from __future__ import annotations

from typing import TypeVar

from synapsecord_core.logging import get_logger

from synapsecord_bot.domains import DomainRegistry, DomainResolverContext
from synapsecord_bot.domains.errors import CircularDomainResolutionError

TDomain =   TypeVar("TDomain")

logger = get_logger(__name__)


class DomainResolutionService:
    def __init__(self, registry: DomainRegistry):
        self._registry = registry

    async def resolve(
            self,
            ctx: DomainResolverContext,
            domain_type: type[TDomain]
    ) -> TDomain | None:
        user_id = getattr(ctx, "discord_user_id", None)

        existing = ctx.domains.get(domain_type)
        if existing is not None:
            logger.debug("domain_resolution_cache_hit", domain=domain_type.__name__)
            return existing

        if ctx.domains.is_resolving(domain_type):
            raise CircularDomainResolutionError(domain_type)

        resolver = self._registry.require(domain_type)
        logger.debug("domain_resolution_started", domain=domain_type.__name__, user_id=user_id)

        ctx.domains.mark_resolving(domain_type)

        try:
            domain = await resolver.resolve(ctx)
        finally:
            ctx.domains.unmark_resolving(domain_type)

        if domain is not None:
            ctx.domains.set(domain)

            logger.debug(
                "domain_resolution_succeeded",
                domain=domain_type.__name__,
                user_id=user_id
            )
        else:
            logger.info(
                "domain_resolution_missing",
                domain=domain_type.__name__,
                user_id=user_id
            )

        return domain
