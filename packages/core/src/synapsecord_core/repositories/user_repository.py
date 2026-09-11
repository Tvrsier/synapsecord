from sqlalchemy import select
from sqlalchemy.orm import Session

from synapsecord_core.db.models import UserModel


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_discord_id(self, discord_id: int) -> UserModel | None:
        statement = select(UserModel).where(UserModel.discord_user_id == discord_id)
        return self._session.scalar(statement)
