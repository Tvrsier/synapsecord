from synapsecord_bot.context.base import SynapseContextMixin
from synapsecord_bot.domains import DomainContext


class FakeContext(SynapseContextMixin):
    def __init__(self):
        self._initialize_synapse_context()


def test_context_initializes_domain_context():
    context = FakeContext()

    assert isinstance(context.domains, DomainContext)

def test_context_domains_are_request_scoped():
    first = FakeContext()
    second = FakeContext()

    assert first.domains is not second.domains