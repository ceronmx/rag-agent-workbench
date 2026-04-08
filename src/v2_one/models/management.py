from v2_one.models.database import engine, Base


def wipe_database():
    """
    Drops all tables and recreates them.
    Use with caution!
    """
    print("Wiping database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database wiped and schema recreated.")


if __name__ == "__main__":
    wipe_database()
