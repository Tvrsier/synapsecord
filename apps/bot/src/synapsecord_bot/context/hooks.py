from synapsecord_bot.context import SynapseAnyContext
from synapsecord_core.logging import get_logger

logger = get_logger(__name__)

async def close_request_scope(ctx: SynapseAnyContext) -> None:
    logger.info("request_scope_closng", user_id=ctx.discord_user_id)
    ctx.close_scope()