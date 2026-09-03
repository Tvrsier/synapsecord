from synapsecord_core.db.session import SessionLocal
from synapsecord_core.logging import get_logger
from synapsecord_core.repositories.game_repository import GameRepository

logger = get_logger(__name__)

INITIAL_GAMES = (
    {
        "slug": "league-of-legends",
        "name": "League of Legends"
    },
)

def seed_games() -> int:
    with SessionLocal() as session:
        repository = GameRepository(session)

        for game_data in INITIAL_GAMES:
            existing = repository.get_by_slug(game_data["slug"])

            if existing is not None:
                logger.info(
                    "game_seed_skipped",
                    slug=game_data["slug"],
                    reason="already_exists"
                )
                continue

            game = repository.create(
                slug=game_data["slug"],
                name=game_data["name"],
            )

            logger.info(
                "game_seed_created",
                game_id=str(game.id),
                slug=game.slug,
                name=game.name,
            )

        session.commit()

    return 0
