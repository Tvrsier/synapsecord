import uuid

import pytest

from synapsecord_bot.context.base import SynapseContextMixin
from synapsecord_bot.domains import RequiredDomainMissingError
from synapsecord_bot.domains.decorators import requires, inject
from synapsecord_core.domain import SynapseUser


class FakeDomainResolutionService:
    def __init__(self, result: object | None) -> None:
        self.result = result
        self.calls: list[tuple[object, type[object]]] = []

    async def resolve(self, ctx: object, domain_type: type[object]) -> object | None:
        self.calls.append((ctx, domain_type))
        return self.result


class FakeServices:
    def __init__(self, result: object | None) -> None:
        self.domain_resolution = FakeDomainResolutionService(result)


class FakeBot:
    def __init__(self, result: object | None) -> None:
        self.services = FakeServices(result)


class FakeContext(SynapseContextMixin):
    def __init__(self, result: object | None) -> None:
        self.bot = FakeBot(result)


@pytest.mark.asyncio
async def test_requires_executes_callback() -> None:
    user = SynapseUser(id=uuid.uuid4(), discord_user_id=123)
    ctx = FakeContext(user)
    called = False

    # noinspection unused-parameter
    @requires(SynapseUser)
    async def callback(context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(ctx)
    assert called

@pytest.mark.asyncio
async def test_requires_raises_when_missing() -> None:
    ctx = FakeContext(None)

    # noinspection unused-parameter
    @requires(SynapseUser)
    async def callback(context: FakeContext) -> None:
        raise AssertionError("Callback should not be executed")

    with pytest.raises(RequiredDomainMissingError) as exc_info:
        await callback(ctx)

    assert exc_info.value.domain_type is SynapseUser

@pytest.mark.asyncio
async def test_inject_executes_callback_when_missing() -> None:
    ctx = FakeContext(None)
    called = False

    # noinspection unused-parameter
    @inject(SynapseUser)
    async def callback(context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(ctx)

    assert called

@pytest.mark.asyncio
async def test_inject_executes_callback() -> None:
    user = SynapseUser(id=uuid.uuid4(), discord_user_id=123)
    ctx = FakeContext(user)
    called = False

    # noinspection unused-parameter
    @inject(SynapseUser)
    async def callback(context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(ctx)
    assert called

@pytest.mark.asyncio
async def test_decorator_find_context() -> None:
    user = SynapseUser(id=uuid.uuid4(), discord_user_id=123)
    ctx = FakeContext(user)
    cog = object()
    called = False

    @requires(SynapseUser)
    async def callback(self: object, context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(cog, ctx)

    assert called

import uuid

import pytest

from synapsecord_bot.context.base import SynapseContextMixin
from synapsecord_bot.domains import RequiredDomainMissingError
from synapsecord_bot.domains.decorators import requires, inject
from synapsecord_core.domain import SynapseUser


class FakeDomainResolutionService:
    def __init__(self, result: object | None) -> None:
        self.result = result
        self.calls: list[tuple[object, type[object]]] = []

    async def resolve(self, ctx: object, domain_type) -> object | None:
        self.calls.append((ctx, domain_type))
        return self.result


class FakeServices:
    def __init__(self, result: object | None) -> None:
        self.domain_resolution = FakeDomainResolutionService(result)


class FakeBot:
    def __init__(self, result: object | None) -> None:
        self.services = FakeServices(result)


class FakeContext(SynapseContextMixin):
    def __init__(self, result: object | None) -> None:
        self.bot = FakeBot(result)


@pytest.mark.asyncio
async def test_requires_executes_callback() -> None:
    user = SynapseUser(id=uuid.uuid4(), discord_user_id=123)
    ctx = FakeContext(user)
    called = False

    # noinspection unused-parameter
    @requires(SynapseUser)
    async def callback(context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(ctx)
    assert called

@pytest.mark.asyncio
async def test_requires_raises_when_missing() -> None:
    ctx = FakeContext(None)

    # noinspection unused-parameter
    @requires(SynapseUser)
    async def callback(context: FakeContext) -> None:
        raise AssertionError("Callback should not be executed")

    with pytest.raises(RequiredDomainMissingError) as exc_info:
        await callback(ctx)

    assert exc_info.value.domain_type is SynapseUser

@pytest.mark.asyncio
async def test_inject_executes_callback_when_missing() -> None:
    ctx = FakeContext(None)
    called = False

    # noinspection unused-parameter
    @inject(SynapseUser)
    async def callback(context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(ctx)

    assert called

@pytest.mark.asyncio
async def test_inject_executes_callback() -> None:
    user = SynapseUser(id=uuid.uuid4(), discord_user_id=123)
    ctx = FakeContext(user)
    called = False

    # noinspection unused-parameter
    @inject(SynapseUser)
    async def callback(context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(ctx)
    assert called

@pytest.mark.asyncio
async def test_decorator_find_context() -> None:
    user = SynapseUser(id=uuid.uuid4(), discord_user_id=123)
    ctx = FakeContext(user)
    cog = object()
    called = False

    @requires(SynapseUser)
    async def callback(self: object, context: FakeContext) -> None:
        nonlocal called
        called = True

    await callback(cog, ctx)

    assert called
