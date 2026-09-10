import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from synapsecord_core.db.models import PlayerProfileModel


class PlayerProfileRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_current_by_game_account_id(self, game_account_id: uuid.UUID) -> PlayerProfileModel:
        statement = (
            select(PlayerProfileModel)
            .where(
                PlayerProfileModel.game_account_id == game_account_id,
                PlayerProfileModel.superseded_at.is_(None)
            )
            .order_by(PlayerProfileModel.version.desc())
        )

        return self._session.scalar(statement)
