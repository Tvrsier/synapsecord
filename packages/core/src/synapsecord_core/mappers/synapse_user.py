from synapsecord_core.db.models import UserModel
from synapsecord_core.domain import SynapseUser


def to_synapse_user(model: UserModel) -> SynapseUser:
    return SynapseUser(
        id=model.id,
        discord_user_id=model.discord_user_id
    )