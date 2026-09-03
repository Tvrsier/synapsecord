import sqlalchemy

from synapsecord_core.db.session import engine


def check_database_connection() -> bool:
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text("SELECT 1"))

        return result.scalar_one() == 1