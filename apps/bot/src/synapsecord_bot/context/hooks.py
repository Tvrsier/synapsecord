from synapsecord_bot.context import SynapseAnyContext


async def close_request_scope(ctx: SynapseAnyContext) -> None:
    ctx.close_scope()