from synapsecord_bot.domains import DomainResolverContext
from synapsecord_core.domain import PlayerProfile, SynapseUser, GameAccount
from synapsecord_core.mappers import to_player_profile
from synapsecord_core.repositories.player_profile_repository import PlayerProfileRepository


class PlayerProfileResolver:
    @staticmethod
    async def resolve(ctx: DomainResolverContext) -> PlayerProfile | None:
        game_account = await ctx.services.domain_resolution.resolve(ctx, GameAccount)
        if game_account is None:
            return None

        repository = PlayerProfileRepository(ctx.scope.session)

        model = repository.get_current_by_game_account_id(game_account.id)

        if model is None:
            return None

        return to_player_profile(model)
