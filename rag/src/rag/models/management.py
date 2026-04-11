from rag.models.database import engine, Base
from rag.utils.logger import logger


def wipe_database():
    """
    Drops all tables and recreates them.
    Use with caution!
    """
    logger.info("Wiping database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database wiped and schema recreated.")


if __name__ == "__main__":
    print("WARNING: This will wipe the entire database.")
    wipe_database()
