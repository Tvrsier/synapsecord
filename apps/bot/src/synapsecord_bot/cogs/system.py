from typing import TYPE_CHECKING

from discord import slash_command
from discord.ext import commands

from synapsecord_bot.context import SynapseApplicationContext
from synapsecord_bot.domains.decorators import requires
from synapsecord_core.domain import SynapseUser

if TYPE_CHECKING:
    from synapsecord_bot.bot import SynapseCORDBot


class System(commands.Cog):
    def __init__(self, bot: SynapseCORDBot):
        self.bot = bot

    @slash_command(name="ping", description="pong")
    async def ping(self, actx: SynapseApplicationContext) -> None:
        latency_ms = round(self.bot.latency * 1000)

        await actx.respond(f"🏓 Pong! `{latency_ms} ms`", ephemeral=True)

    @slash_command(name="whoami", description="Retrieve your information")
    @requires(SynapseUser)
    async def whoami(self, actx: SynapseApplicationContext) -> None:
        await actx.respond(f"Hello, {actx.synapse_user.id}!", ephemeral=True)

def setup(bot: SynapseCORDBot):
    bot.add_cog(System(bot))