from dataclasses import dataclass

import pytest
from synapsecord_bot.domains import (
    DomainContext,
    DomainRegistry,
    DomainResolutionService,
)
from synapsecord_bot.domains.errors import CircularDomainResolutionError


@dataclass
class ExampleDomain:
    value: str


class FakeContext:
    def __init__(self) -> None:
        self.domains = DomainContext()


class ExampleResolver:
    def __init__(self) -> None:
        self.calls = 0

    async def resolve(self, ctx: object) -> ExampleDomain | None:
        self.calls += 1
        return ExampleDomain(value="resolved")


@pytest.mark.asyncio
async def test_resolve_domain() -> None:
    registry = DomainRegistry()
    resolver = ExampleResolver()
    registry.register(ExampleDomain, resolver)

    service = DomainResolutionService(registry)
    ctx = FakeContext()

    domain = await service.resolve(ctx, ExampleDomain)

    assert domain == ExampleDomain(value="resolved")
    assert ctx.domains.get(ExampleDomain) is domain


@pytest.mark.asyncio
async def test_resolve_uses_cached_domain() -> None:
    registry = DomainRegistry()
    resolver = ExampleResolver()
    registry.register(ExampleDomain, resolver)

    service = DomainResolutionService(registry)
    ctx = FakeContext()

    first = await service.resolve(ctx, ExampleDomain)
    second = await service.resolve(ctx, ExampleDomain)

    assert second is first
    assert resolver.calls == 1


class MissingResolver:
    async def resolve(self, ctx: object) -> ExampleDomain | None:
        return None


@pytest.mark.asyncio
async def test_resolve_returns_none_when_domain_cannot_be_resolved() -> None:
    registry = DomainRegistry()
    registry.register(ExampleDomain, MissingResolver())

    service = DomainResolutionService(registry)
    ctx = FakeContext()

    domain = await service.resolve(ctx, ExampleDomain)

    assert domain is None
    assert ctx.domains.get(ExampleDomain) is None


@dataclass
class DomainA:
    value: str = "a"


@dataclass
class DomainB:
    value: str = "b"


class DomainAResolver:
    def __init__(self, service: DomainResolutionService) -> None:
        self._service = service

    async def resolve(self, ctx: object) -> DomainA | None:
        await self._service.resolve(ctx, DomainB)
        return DomainA()


class DomainBResolver:
    def __init__(self, service: DomainResolutionService) -> None:
        self._service = service

    async def resolve(self, ctx: object) -> DomainB | None:
        await self._service.resolve(ctx, DomainA)
        return DomainB()


@pytest.mark.asyncio
async def test_circular_domain_resolution_raises() -> None:
    registry = DomainRegistry()
    service = DomainResolutionService(registry)

    registry.register(DomainA, DomainAResolver(service))
    registry.register(DomainB, DomainBResolver(service))

    ctx = FakeContext()

    with pytest.raises(CircularDomainResolutionError) as exc_info:
        await service.resolve(ctx, DomainA)

    assert exc_info.value.domain_type is DomainA
    assert not ctx.domains.is_resolving(DomainA)
    assert not ctx.domains.is_resolving(DomainB)
