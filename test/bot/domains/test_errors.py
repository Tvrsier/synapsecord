import pytest
from discord import ApplicationCommandError
from discord.ext.commands import CommandError

from synapsecord_bot.domains import RequiredDomainMissingError
from synapsecord_core.domain import SynapseUser

from synapsecord_bot.errors.handlers import (
    handle_application_command_error,
    handle_command_error,
)


class FakeCommandContext:
    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, float | None]] = []

    async def send(
        self,
        message: str,
        *,
        delete_after: float | None = None,
    ) -> None:
        self.sent_messages.append(
            (message, delete_after)
        )


# noinspection method-may-be-static
class FakeResponse:
    def is_done(self) -> bool:
        return False


class FakeApplicationContext:
    def __init__(self) -> None:
        self.response = FakeResponse()
        self.responses: list[tuple[str, bool]] = []

    async def respond(
        self,
        message: str,
        *,
        ephemeral: bool = False,
    ) -> None:
        self.responses.append((message, ephemeral))


class FakeRespondedApplicationContext:
    def __init__(self) -> None:
        self.response = FakeDoneResponse()
        self.followup = FakeFollowup()


# noinspection method-may-be-static
class FakeDoneResponse:
    def is_done(self) -> bool:
        return True


class FakeFollowup:
    def __init__(self) -> None:
        self.messages: list[tuple[str, bool]] = []

    async def send(
        self,
        message: str,
        *,
        ephemeral: bool = False,
    ) -> None:
        self.messages.append((message, ephemeral))


def test_required_domain_is_command_error():
    assert issubclass(RequiredDomainMissingError, CommandError)

def test_required_domain_is_application_command_error():
    assert issubclass(RequiredDomainMissingError, ApplicationCommandError)

@pytest.mark.asyncio
async def test_command_error_handler_sends_required_domain_message() -> None:
    ctx = FakeCommandContext()
    error = RequiredDomainMissingError(SynapseUser)

    await handle_command_error(ctx, error)  # type: ignore[arg-type]

    assert len(ctx.sent_messages) == 1

    message, delete_after = ctx.sent_messages[0]

    assert "SynapseUser" in message
    assert delete_after == 20

@pytest.mark.asyncio
async def test_application_error_handler_responds_ephemerally() -> None:
    ctx = FakeApplicationContext()
    error = RequiredDomainMissingError(SynapseUser)

    await handle_application_command_error(  # type: ignore[arg-type]
        ctx,
        error,
    )

    assert len(ctx.responses) == 1

    message, ephemeral = ctx.responses[0]

    assert "SynapseUser" in message
    assert ephemeral is True

@pytest.mark.asyncio
async def test_application_error_handler_uses_followup_when_already_responded() -> None:
    ctx = FakeRespondedApplicationContext()
    error = RequiredDomainMissingError(SynapseUser)

    await handle_application_command_error(  # type: ignore[arg-type]
        ctx,
        error,
    )

    assert len(ctx.followup.messages) == 1

    message, ephemeral = ctx.followup.messages[0]

    assert "SynapseUser" in message
