import os
import uuid
import shutil
from app.worker import process_video_task
import cv2

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schema import VideoRecord
from app.config import settings


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)


def extract_video_metadata(video_path: str):
    """
    Extract basic metadata from the uploaded video.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open uploaded video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = 0.0

    if fps and fps > 0:
        duration = total_frames / fps

    cap.release()

    return {
        "fps": float(fps),
        "total_frames": total_frames,
        "duration": round(duration, 2),
    }


@router.post("/upload")
def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    # Only allow video files
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=400,
            detail="Only video files are allowed."
        )

    # Create unique video ID
    video_id = str(uuid.uuid4())

    # Ensure upload directory exists
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)

    # Build safe local path
    safe_filename = f"{video_id}_{file.filename}"
    video_path = os.path.abspath(
        os.path.join(
            settings.STORAGE_DIR,
            safe_filename
        )
    )

    try:
        # Save uploaded file in chunks
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
                length=1024 * 1024
            )

        # Extract video metadata
        metadata = extract_video_metadata(video_path)

        # Create database record
        video_record = VideoRecord(
            id=video_id,
            filename=file.filename,
            status="QUEUED",
            duration=metadata["duration"],
            fps=metadata["fps"],
            total_frames=metadata["total_frames"],
        )

        db.add(video_record)
        db.commit()

        process_video_task.delay(
           video_id,
           video_path
        )

        return {
            "message": "Video uploaded successfully.",
            "video_id": video_id,
            "filename": file.filename,
            "status": "QUEUED",
            "metadata": metadata,
        }

    except Exception as e:

        db.rollback()

        # Delete failed upload
        if os.path.exists(video_path):
            os.remove(video_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/{video_id}/status")
def get_video_status(
    video_id: str,
    db: Session = Depends(get_db),
):

    video = (
        db.query(VideoRecord)
        .filter(VideoRecord.id == video_id)
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    return {
        "video_id": video.id,
        "filename": video.filename,
        "status": video.status,
        "duration": video.duration,
    }

@router.get("/{video_id}/summary")
def get_video_summary(
    video_id: str,
    db: Session = Depends(get_db),
):

    video = (
        db.query(VideoRecord)
        .filter(
            VideoRecord.id == video_id
        )
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    return {
        "video_id": video.id,

        "filename": video.filename,

        "status": video.status,

        "duration": video.duration,

        "summary": video.summary,
    }