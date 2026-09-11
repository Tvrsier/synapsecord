import discord
from discord import ApplicationContext, Interaction

from synapsecord_bot.context.base import SynapseContextMixin


class SynapseApplicationContext(SynapseContextMixin, ApplicationContext):
    def __init__(self, bot: discord.Bot, itx: Interaction):
        super().__init__(bot, itx)
        self._initialize_synapse_context()
