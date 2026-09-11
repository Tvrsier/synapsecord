from discord.ext import commands

from synapsecord_bot.context import SynapseContext, SynapseApplicationContext
from synapsecord_bot.errors.messages import get_error_message


async def handle_command_error(ctx: SynapseContext, error: commands.CommandError) -> None:
    message = get_error_message(error)

    if message is None:
        raise error

    await ctx.send(message, delete_after=20)


async def handle_application_command_error(ctx: SynapseApplicationContext, error: commands.CommandError) -> None:
    message = get_error_message(error)

    if message is None:
        raise error

    if ctx.response.is_done():
        await ctx.followup.send(message, ephemeral=True)
    else:
        await ctx.respond(message, ephemeral=True)
