from sqlalchemy import select
from sqlalchemy.orm import Session

from synapsecord_core.db.models import Game


class GameRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_slug(self, slug: str) -> Game | None:
        statement = select(Game).where(Game.slug == slug)
        return self._session.scalar(statement)

    def create(
            self,
            *,
            slug: str,
            name: str,
            enabled: bool = True,
    ) -> Game:
        game = Game(
            slug=slug,
            name=name,
            enabled=enabled,
        )

        self._session.add(game)
        self._session.flush()

        return game
