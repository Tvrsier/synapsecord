from __future__ import annotations

import argparse
import sys

from synapsecord_core.commands.seed_games import seed_games
from synapsecord_core.config import get_settings
from synapsecord_core.db.health import check_database_connection
from synapsecord_core.logging import configure_logging, get_logger

logger = get_logger(__name__)

def health() -> int:
    settings = get_settings()
    
    logger.info("profiler_health_started", environment=settings.synapsecord_env)
    
    try:
        database_ok = check_database_connection()
    except Exception as e:  # noqa: BLE001
        logger.error("database_health_check_failed", error=str(e))
        return 1
    
    if not database_ok:
        logger.error("database_health_check_failed")
        return 1
    
    logger.info("database_health_check_succeeded")
    
    return 0


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(
        prog="synapsecord-profiler",
        description="SynapseCORD player profiling engine.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health", help="Check profiler dependencies.")

    subparsers.add_parser("seed-games", help="Seed games into the database.")

    args = parser.parse_args()

    match args.command:
        case "health":
            sys.exit(health())

        case "seed-games":
            sys.exit(seed_games())


if __name__ == "__main__":
    main()