from __future__ import annotations

import pkgutil

import discord
from discord import DiscordException
from discord.ext import commands
from discord.ext.commands import Context

from synapsecord_bot.context.hooks import close_request_scope
from synapsecord_bot.errors.handlers import handle_command_error
from synapsecord_core.config import get_settings
from synapsecord_core.logging import get_logger

from synapsecord_bot.bot.ready import ReadyState
from synapsecord_bot.context import SynapseApplicationContext, SynapseContext
from synapsecord_bot.services.container import ServiceContainer

logger = get_logger(__name__)


class SynapseCORDBot(commands.Bot):
    def __init__(self):
        self.settings = get_settings()
        self.ready_state = ReadyState()
        self.services = ServiceContainer()

        intents = discord.Intents.default()

        debug_guilds = (
            [self.settings.discord_guild_id]
            if self.settings.discord_guild_id is not None
            else None
        )

        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned,
            help_command=None,
            debug_guilds=debug_guilds,
            auto_sync_commands=True,
        )

        self.after_invoke(close_request_scope)

        logger.info("bot_setup_started")

        self._load_cogs()

        logger.info("bot_setup_completed", extensions=list(self.extensions))

    def _load_cogs(self) -> None:
        import synapsecord_bot.cogs as cogs_package

        prefix = f"{cogs_package.__name__}."

        for module in pkgutil.iter_modules(cogs_package.__path__, prefix):
            extension = module.name
            component = extension.rsplit(".", maxsplit=1)[-1]

            self.ready_state.register(component)
            logger.info("cog_loading", extension=extension)

            try:
                self.load_extension(extension)
            except Exception:
                logger.exception("cog_load_failed", extension=extension)
                raise

            self.ready_state.mark_ready(component)

            logger.info("cog_loaded", extension=extension)

    async def on_ready(self) -> None:
        user = self.user

        logger.info(
            "bot_connected",
            user_id=user.id if user is not None else None,
            username=str(user) if user is not None else None,
            guild_count=len(self.guilds),
            pending_components=sorted(self.ready_state.pending),
        )

    async def get_context(
            self,
            message: discord.Message,
            *,
            cls: type[Context] = SynapseContext
    ) -> SynapseContext:
        return await super().get_context(message, cls=cls)

    async def get_application_context(
            self,
            interaction: discord.Interaction,
            cls=SynapseApplicationContext
    ) -> SynapseApplicationContext:
        return await super().get_application_context(interaction, cls=cls)

    # noinspection method-overriding
    async def on_command_error(self, ctx: SynapseContext, error: commands.CommandError) -> None:
        await handle_command_error(ctx, error)

    # noinspection method-overriding
    async def on_application_command_error(self, ctx: SynapseApplicationContext, error: DiscordException) -> None:
        await handle_command_error(ctx, error)