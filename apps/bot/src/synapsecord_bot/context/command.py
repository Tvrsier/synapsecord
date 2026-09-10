from discord.ext.commands import Context

from synapsecord_bot.context.base import SynapseContextMixin


class SynapseContext(SynapseContextMixin, Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_synapse_context()
