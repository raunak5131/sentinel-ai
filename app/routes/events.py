from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.schema import EventRecord


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/video/{video_id}")
def get_video_events(video_id: str):

    db = SessionLocal()

    try:

        events = (
            db.query(EventRecord)
            .filter(
                EventRecord.video_id == video_id
            )
            .order_by(
                EventRecord.start_timestamp.asc()
            )
            .all()
        )

        return {

            "video_id": video_id,

            "total_events": len(events),

            "events": [

                {

                    "id": str(event.id),

                    "start_timestamp":
                        event.start_timestamp,

                    "end_timestamp":
                        event.end_timestamp,

                    "event_type":
                        event.event_type,

                    "entity_id":
                        event.entity_id,

                    "object_class":
                        event.object_class,

                    "confidence":
                        event.confidence,

                    "anomaly_score":
                        event.anomaly_score,

                    "description":
                        event.description,

                    "metadata":
                        event.metadata_json,

                }

                for event in events
            ],
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:

        db.close()