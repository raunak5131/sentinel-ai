from sqlalchemy import text

from app.database import engine


def test_database():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database();")
            )

            database_name = result.scalar()

            print("SUCCESS!")
            print(f"Connected to database: {database_name}")

    except Exception as e:
        print("DATABASE CONNECTION FAILED")
        print(e)


if __name__ == "__main__":
    test_database()