from __future__ import annotations

from typing import TypeVar, cast, Any

from synapsecord_bot.domains.errors import (
    DomainResolverAlreadyRegisteredError,
    DomainResolverNotRegisteredError,
)
from synapsecord_bot.domains.resolver import DomainResolver

TDomain = TypeVar("TDomain")


class DomainRegistry:
    def __init__(self):
        self._resolvers: dict[type[object], DomainResolver[Any]] = {}

    def register(
            self,
            domain_type: type[TDomain],
            resolver: DomainResolver[TDomain]
    ) -> None:
        if domain_type in self._resolvers:
            raise DomainResolverAlreadyRegisteredError(domain_type)

        self._resolvers[domain_type] = resolver

    # noinspection unnecessary-cast
    def get(self, domain_type: type[TDomain]) -> DomainResolver[TDomain] | None:
        resolver = self._resolvers.get(domain_type)

        return None if resolver is None else cast(DomainResolver[TDomain], resolver)

    def require(self, domain_type: type[TDomain]) -> DomainResolver[TDomain]:
        resolver = self.get(domain_type)

        if resolver is None:
            raise DomainResolverNotRegisteredError(domain_type)

        return resolver