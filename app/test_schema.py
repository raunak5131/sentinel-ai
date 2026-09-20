from app.database import SessionLocal
from app.models.schema import VideoRecord


def test_schema():
    db = SessionLocal()

    try:
        video = VideoRecord(
            filename="test_video.mp4",
            status="TEST"
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        print("SUCCESS!")
        print(f"Video ID: {video.id}")
        print(f"Filename: {video.filename}")
        print(f"Status: {video.status}")

        db.delete(video)
        db.commit()

        print("Test record deleted successfully.")

    except Exception as e:
        db.rollback()
        print("TEST FAILED")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    test_schema()