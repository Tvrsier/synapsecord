from __future__ import annotations

from synapsecord_core.logging import configure_logging, get_logger

from synapsecord_bot.bot import SynapseCORDBot

logger = get_logger(__name__)

def main() -> None:
    configure_logging()

    bot = SynapseCORDBot()

    if not bot.settings.discord_bot_token:
        logger.error("discord_bot_token_missing")
        raise RuntimeError("DISCORD_BOT_TOKEN is not configured")

    logger.info("bot_starting", environment=bot.settings.synapsecord_env)

    bot.run(
        bot.settings.discord_bot_token,
        log_handler=None
    )
    
if __name__ == "__main__":
    main()