from rag.models.database import engine
from sqlalchemy import text


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful!")

            # Verify pgvector
            result = connection.execute(
                text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            )
            ext = result.fetchone()
            if ext:
                print(f"Extension '{ext[0]}' is present.")
            else:
                print("Extension 'vector' not found.")
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    test_connection()
