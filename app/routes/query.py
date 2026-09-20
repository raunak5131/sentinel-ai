from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.qa_service import VideoQAService


router = APIRouter(
    prefix="/videos",
    tags=["Video Q&A"],
)


class QueryRequest(BaseModel):
    question: str
    limit: int = 8


@router.post("/{video_id}/query")
def query_video(video_id: str, request: QueryRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        service = VideoQAService()

        result = service.answer(
            video_id=video_id,
            question=request.question,
            limit=request.limit,
        )

        return {
            "video_id": video_id,
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"],
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )