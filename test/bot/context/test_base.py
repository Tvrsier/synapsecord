import uuid

import pytest

from synapsecord_bot.context.base import SynapseContextMixin
from synapsecord_bot.domains import MissingDomainError
from synapsecord_bot.services.scope import ApplicationScope
from synapsecord_core.domain import SynapseUser


class FakeSessionFactory:
    def __call__(self):
        raise AssertionError("Session should not be created by context initialization.")


# noinspection method-may-be-static
class FakeServices:
    def create_scope(self) -> ApplicationScope:
        return ApplicationScope(
            session_factory=FakeSessionFactory(),  # type: ignore[arg-type]
        )


class FakeBot:
    def __init__(self) -> None:
        self.services = FakeServices()


class FakeContext(SynapseContextMixin):
    def __init__(self) -> None:
        self.bot = FakeBot()
        self._initialize_synapse_context()


def test_context_initializes_domain_context() -> None:
    context = FakeContext()

    assert context.domains is context.scope.domains


def test_context_domains_are_request_scoped() -> None:
    first = FakeContext()
    second = FakeContext()

    assert first.domains is not second.domains


def test_context_scope_is_request_scoped() -> None:
    first = FakeContext()
    second = FakeContext()

    assert first.scope is not second.scope

def test_context_exposes_required_domain() -> None:
    context = FakeContext()

    user = SynapseUser(
        id=uuid.uuid4(),
        discord_user_id=123456789,
    )

    context.domains.set(user)

    assert context.synapse_user is user

def test_context_raises_when_required_domain_is_missing() -> None:
    context = FakeContext()

    with pytest.raises(MissingDomainError):
        _ = context.synapse_user
