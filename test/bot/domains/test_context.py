from dataclasses import dataclass

import pytest
from synapsecord_bot.domains import DomainContext
from synapsecord_bot.domains.errors import MissingDomainError


@dataclass
class ExampleDomain:
    value: str


def test_set_and_get_domain():
    context = DomainContext()
    domain = ExampleDomain(value="test")

    context.set(domain)

    assert context.get(ExampleDomain) is domain

def test_get_missing_domain_returns_none():
    context = DomainContext()

    assert context.get(ExampleDomain) is None

def test_require_missing_domain_raises():
    context = DomainContext()

    with pytest.raises(MissingDomainError):
        context.require(ExampleDomain)
