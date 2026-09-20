from sqlalchemy import text

from app.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models.schema import VideoRecord, EventRecord


def init_database():
    print("Initializing SentinelAI database...")

    with engine.begin() as connection:
        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector;")
        )

    Base.metadata.create_all(bind=engine)

    print("SUCCESS: Database initialized.")
    print("Tables created: videos, events")
    print("pgvector extension ready.")


if __name__ == "__main__":
    init_database()