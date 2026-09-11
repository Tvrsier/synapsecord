from synapsecord_bot.domains import DomainResolverContext
from synapsecord_core.domain import SynapseUser
from synapsecord_core.mappers import to_synapse_user
from synapsecord_core.repositories.user_repository import UserRepository


class SynapseUserResolver:
    @staticmethod
    async def resolve(ctx: DomainResolverContext) -> SynapseUser | None:
        repository = UserRepository(ctx.scope.session)

        model = repository.get_by_discord_id(ctx.discord_user_id)

        if model is None:
            return None

        return to_synapse_user(model)
