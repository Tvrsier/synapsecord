import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from synapsecord_bot.context.base import SynapseContextMixin
from synapsecord_bot.domains import DomainRegistry, DomainResolutionService
from synapsecord_bot.domains.decorators import requires
from synapsecord_bot.domains.resolvers import (
    GameAccountResolver,
    PlayerProfileResolver,
    SynapseUserResolver,
)
from synapsecord_bot.services.scope import ApplicationScope
from synapsecord_core.domain import (
    GameAccount,
    PlayerProfile,
    SynapseUser,
)


class FakeSession:
    def close(self) -> None:
        pass


class FakeServices:
    def __init__(self) -> None:
        registry = DomainRegistry()

        registry.register(
            SynapseUser,
            SynapseUserResolver(),
        )
        registry.register(
            GameAccount,
            GameAccountResolver(),
        )
        registry.register(
            PlayerProfile,
            PlayerProfileResolver(),
        )

        self.domain_resolution = DomainResolutionService(registry)


class FakeBot:
    def __init__(self) -> None:
        self.services = FakeServices()


class FakeAuthor:
    id = 123456789


class FakeContext(SynapseContextMixin):
    def __init__(self) -> None:
        self.bot = FakeBot()
        self.author = FakeAuthor()
        self._scope = ApplicationScope(
            session_factory=lambda: FakeSession(),  # type: ignore[arg-type]
        )


@pytest.mark.asyncio
async def test_requires_player_profile_resolves_dependency_chain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_id = uuid.uuid4()
    game_account_id = uuid.uuid4()
    profile_id = uuid.uuid4()
    game_id = uuid.uuid4()
    now = datetime.now(UTC)

    user_model = SimpleNamespace(
        id=user_id,
        discord_user_id=123456789,
    )

    game_account_model = SimpleNamespace(
        id=game_account_id,
        user_id=user_id,
        game_id=game_id,
        external_id="player-123",
        display_name="Player",
        region="EUW",
        verified_at=now,
    )

    player_profile_model = SimpleNamespace(
        id=profile_id,
        game_account_id=game_account_id,
        version=1,
        status="ready",
        confidence=0.95,
        valid_from=now,
        superseded_at=None,
    )

    # noinspection method-may-be-static,unused-parameter
    class FakeUserRepository:
        def __init__(self, session: object) -> None:
            pass

        def get_by_discord_id(
            self,
            discord_user_id: int,
        ) -> object | None:
            assert discord_user_id == 123456789
            return user_model

    # noinspection unused-parameter,method-may-be-static
    class FakeGameAccountRepository:
        def __init__(self, session: object) -> None:
            pass

        def get_by_user_id(
            self,
            requested_user_id: uuid.UUID,
        ) -> object | None:
            assert requested_user_id == user_id
            return game_account_model

    # noinspection unused-parameter,method-may-be-static
    class FakePlayerProfileRepository:
        def __init__(self, session: object) -> None:
            pass

        def get_current_by_game_account_id(
            self,
            requested_game_account_id: uuid.UUID,
        ) -> object | None:
            assert requested_game_account_id == game_account_id
            return player_profile_model

    monkeypatch.setattr(
        "synapsecord_bot.domains.resolvers.synapse_user.UserRepository",
        FakeUserRepository,
    )
    monkeypatch.setattr(
        "synapsecord_bot.domains.resolvers.game_account.GameAccountRepository",
        FakeGameAccountRepository,
    )
    monkeypatch.setattr(
        "synapsecord_bot.domains.resolvers.player_profile.PlayerProfileRepository",
        FakePlayerProfileRepository,
    )

    ctx = FakeContext()

    @requires(PlayerProfile)
    async def callback(context: FakeContext) -> None:
        assert context.synapse_user.id == user_id
        assert context.game_account.id == game_account_id
        assert context.player_profile.id == profile_id

    await callback(ctx)