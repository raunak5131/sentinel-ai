from app.database import SessionLocal
from app.models.schema import EventRecord
from app.ai.event_embedder import EventEmbedder


class EventIndexer:

    def __init__(self):
        self.embedder = EventEmbedder()

    def index_video(self, video_id):
        db = SessionLocal()

        try:
            events = (
                db.query(EventRecord)
                .filter(EventRecord.video_id == video_id)
                .filter(EventRecord.embedding.is_(None))
                .order_by(EventRecord.start_timestamp)
                .all()
            )

            print(f"Found {len(events)} events to index.")

            indexed = 0

            for event in events:

                text = self.embedder.create_event_text(event)

                embedding = self.embedder.embed(text)

                event.embedding = embedding

                indexed += 1

                print(
                    f"Indexed event {event.id} "
                    f"at {event.start_timestamp:.2f}s"
                )

            db.commit()

            return {
                "video_id": video_id,
                "indexed_events": indexed,
            }

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()