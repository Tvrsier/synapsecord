from synapsecord_core.logging import get_logger

from synapsecord_bot.context import SynapseAnyContext

logger = get_logger(__name__)

async def close_request_scope(ctx: SynapseAnyContext) -> None:
    logger.debug("request_scope_closing", user_id=ctx.discord_user_id)
    ctx.close_scope()