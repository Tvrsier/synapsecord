from sqlalchemy import select
from sqlalchemy.orm import Session

from synapsecord_core.db.models import UserModel
from synapsecord_core.logging import get_logger

logger = get_logger(__name__)


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_discord_id(self, discord_id: int) -> UserModel | None:
        logger.debug("user_lookup_by_discord_id", discord_id=discord_id)
        statement = select(UserModel).where(UserModel.discord_user_id == discord_id)
        user = self._session.scalar(statement)

        logger.debug("user_lookup_completed", discord_id=discord_id, found=user is not None)
        return user
