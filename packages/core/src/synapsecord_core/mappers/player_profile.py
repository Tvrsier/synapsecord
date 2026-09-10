from synapsecord_core.db.models import PlayerProfileModel
from synapsecord_core.domain.player_profile import PlayerProfile


def to_player_profile(model: PlayerProfileModel) -> PlayerProfile:
    return PlayerProfile(
        id=model.id,
        game_account_id=model.game_account_id,
        version=model.version,
        status=model.status,
        confidence=model.confidence,
        valid_from=model.valid_from,
        superseded_at=model.superseded_at,
    )
