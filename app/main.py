import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.events import router as events_router
from app.config import settings
from app.database import engine
from sqlalchemy import text
from app.routes.query import router as query_router

from app.api import routes_video


os.makedirs(settings.STORAGE_DIR, exist_ok=True)


app = FastAPI(
    title="SentinelAI",
    description="Temporal Video Intelligence System",
    version="0.3.0"
)

app.include_router(events_router)
app.include_router(query_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes_video.router)
app.include_router(query_router)

@app.get("/")
def root():

    return {
        "message": "SentinelAI API is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():

    database_status = "connected"

    try:
        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )

    except Exception:
        database_status = "disconnected"

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "database": database_status
    }