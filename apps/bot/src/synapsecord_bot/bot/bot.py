from __future__ import annotations

import pkgutil

import discord
from discord.ext import commands
from synapsecord_core.config import get_settings
from synapsecord_core.logging import get_logger

from synapsecord_bot.bot.ready import ReadyState

logger = get_logger(__name__)


class SynapseCORDBot(commands.Bot):
    def __init__(self):
        self.settings = get_settings()
        self.ready_state = ReadyState()

        intents = discord.Intents.default()

        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned,
            help_command=None
        )

    async def setup_hook(self) -> None:
        logger.info("bot_setup_started")

        await self._load_cogs()
        await self._sync_application_commands()

        logger.info("bot_setup_completed", extensions=list(self.extensions))

    async def _load_cogs(self) -> None:
        import synapsecord_bot.cogs as cogs_package

        prefix = f"{cogs_package.__name__}."

        for module in pkgutil.iter_modules(cogs_package.__path__, prefix):
            extension = module.name

            try:
                await self.load_extension(extension)
            except Exception:
                logger.exception("cog_load_failed", extension=extension)
                raise

            logger.info("cog_loaded", extension=extension)

    async def _sync_application_commands(self) -> None:
        if self.settings.discord_guild_id is not None:
            guild = discord.Object(id=self.settings.discord_guild_id)

            self.tree.copy_global_to(guild=guild)

            commands_synced = await self.tree.sync(guild=guild)

            logger.info(
                "application_command_synced",
                scope="guild",
                guild_id=guild.id,
                count=len(commands_synced)
            )

            return

        commands_synced = await self.tree.sync()

        logger.info(
            "application_command_synced",
            scope="global",
            count=len(commands_synced)
        )

    async def on_ready(self) -> None:
        logger.info(
            "bot_connected",
            user_id=self.user.id if self.user else None,
            username=str(self.user) if self.user else None,
            guild_count=len(self.guilds),
            pending_components=sorted(self.ready_state.pending)
        )