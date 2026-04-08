import argparse
from v2_one.models.database import engine, Base
from v2_one.models.management import wipe_database


def main():
    parser = argparse.ArgumentParser(description="v2-one RAG Project")
    parser.add_argument(
        "--test-mode", action="store_true", help="Wipe database on startup for testing."
    )
    args = parser.parse_args()

    print("Starting v2-one...")

    if args.test_mode:
        wipe_database()
    else:
        # Just ensure tables are created
        Base.metadata.create_all(bind=engine)
        print("Database schema verified.")

    print("Application is ready.")


if __name__ == "__main__":
    main()
