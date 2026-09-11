from synapsecord_bot.domains import DomainResolverContext
from synapsecord_core.domain import GameAccount, SynapseUser
from synapsecord_core.mappers import to_game_account
from synapsecord_core.repositories.game_account_repository import GameAccountRepository


class GameAccountResolver:
    @staticmethod
    async def resolve(ctx: DomainResolverContext) -> GameAccount | None:
        synapse_user = await ctx.services.domain_resolution.resolve(ctx, SynapseUser)

        if synapse_user is None:
            return None

        repository = GameAccountRepository(ctx.scope.session)

        model = repository.get_by_user_id(synapse_user.id)

        if model is None:
            return None

        return to_game_account(model)