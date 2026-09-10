from synapsecord_core.db.models import GameAccountModel
from synapsecord_core.domain.game_account import GameAccount


def to_game_account(model: GameAccountModel) -> GameAccount:
    return GameAccount(
        id=model.id,
        user_id=model.user_id,
        game_id=model.game_id,
        external_id=model.external_id,
        display_name=model.display_name,
        region=model.region,
        verified_at=model.verified_at,
    )
