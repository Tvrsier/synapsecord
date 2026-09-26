from synapsecord_bot.context import SynapseApplicationContext, SynapseContext
from synapsecord_bot.context.base import SynapseContextMixin


def test_synapse_context_uses_synapse_context_mixin():
    assert issubclass(SynapseContext, SynapseContextMixin)

def test_synapse_application_context_uses_synapse_context_mixin():
    assert issubclass(SynapseApplicationContext, SynapseContextMixin)
