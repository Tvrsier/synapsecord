import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from synapsecord_core.db.models import GameAccountModel


class GameAccountRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_user_id(self, user_id: uuid.UUID) -> GameAccountModel | None:
        statement = select(GameAccountModel).where(GameAccountModel.user_id == user_id)
        return self._session.scalar(statement)
