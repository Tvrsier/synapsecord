from dataclasses import dataclass

import pytest

from apps.bot.src.synapsecord_bot.domains import (
    DomainRegistry,
    DomainResolverAlreadyRegisteredError,
    DomainResolverNotRegisteredError,
)


@dataclass
class ExampleDomain:
    value: str


class ExampleResolver:
    async def resolve(self, ctx: object) -> ExampleDomain | None:
        return ExampleDomain(value="test")


def test_register_and_get_resolver() -> None:
    registry = DomainRegistry()
    resolver = ExampleResolver()

    registry.register(ExampleDomain, resolver)

    assert registry.get(ExampleDomain) is resolver


def test_get_unregistered_resolver_returns_none() -> None:
    registry = DomainRegistry()

    assert registry.get(ExampleDomain) is None


def test_require_unregistered_resolver_raises() -> None:
    registry = DomainRegistry()

    with pytest.raises(DomainResolverNotRegisteredError) as exc_info:
        registry.require(ExampleDomain)

    assert exc_info.value.domain_type is ExampleDomain


def test_register_duplicate_resolver_raises() -> None:
    registry = DomainRegistry()
    resolver = ExampleResolver()

    registry.register(ExampleDomain, resolver)

    with pytest.raises(DomainResolverAlreadyRegisteredError):
        registry.register(ExampleDomain, resolver)