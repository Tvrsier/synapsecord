from __future__ import annotations

from typing import TypeVar, cast

from synapsecord_bot.domains.errors import MissingDomainError

TDomain = TypeVar("TDomain")


class DomainContext:
    def __init__(self):
        self._domains: dict[type[object], object] = {}
        self._resolving: set[type[object]] = set()
        
    def set(self, domain: TDomain) -> None:
        self._domains[type(domain)] = domain
        
    def get(self, domain_type: type[TDomain]) -> TDomain | None:
        domain = self._domains.get(domain_type, None)
        
        return None if domain is None else cast(TDomain, domain)

    def require(self, domain_type: type[TDomain]) -> TDomain:
        domain = self.get(domain_type)

        if domain is None:
            raise MissingDomainError(domain_type)

        return domain

    def is_resolving(self, domain_type: type[object]) -> bool:
        return domain_type in self._resolving

    def mark_resolving(self, domain_type: type[object]) -> None:
        self._resolving.add(domain_type)

    def unmark_resolving(self, domain_type: type[object]) -> None:
        self._resolving.remove(domain_type)