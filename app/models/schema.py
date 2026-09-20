import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    Integer,
    Text
)
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from app.database import Base


class VideoRecord(Base):
    __tablename__ = "videos"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    filename = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="QUEUED",
        index=True
    )

    duration = Column(
        Float,
        nullable=True
    )

    fps = Column(
        Float,
        nullable=True
    )

    total_frames = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    summary = Column(
        Text,
        nullable=True,
    )


class EventRecord(Base):
    __tablename__ = "events"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    video_id = Column(
        String,
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    start_timestamp = Column(
        Float,
        nullable=False,
        index=True
    )

    end_timestamp = Column(
        Float,
        nullable=True
    )

    event_type = Column(
        String,
        nullable=False,
        index=True
    )

    entity_id = Column(
        String,
        nullable=False,
        index=True
    )

    object_class = Column(
        String,
        nullable=True
    )

    confidence = Column(
        Float,
        default=1.0
    )

    anomaly_score = Column(
        Float,
        nullable=True
    )

    description = Column(
        String,
        nullable=False
    )

    metadata_json = Column(
        JSON,
        default=dict
    )

    embedding = Column(
        Vector(384),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )