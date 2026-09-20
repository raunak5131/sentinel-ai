<h1 align="center">👁️ SentinelAI</h1>
<p align="center">
  <strong>AI-Powered Video Intelligence & Temporal RAG</strong>
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI"></a>
  <a href="https://ultralytics.com/"><img src="https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge&logo=ultralytics&logoColor=black" alt="YOLO"></a>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://github.com/pgvector/pgvector"><img src="https://img.shields.io/badge/pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="pgvector"></a>
  <a href="https://docs.celeryq.dev/"><img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery"></a>
  <a href="https://redis.io/"><img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"></a>
  <a href="https://reactjs.org/"><img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"></a>
</p>

<p align="center">
  Transform long, dense video feeds into structured, searchable, and explainable intelligence using Computer Vision, Event State Engines, and Temporal RAG.
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#system-architecture">Architecture</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#technology-stack">Tech Stack</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#api-endpoints">API Reference</a>
</p>

---

## Overview

**SentinelAI** is an end-to-end video intelligence engine built for long surveillance and industrial video feeds. Instead of overwhelming an LLM with massive, raw frame sequences, SentinelAI extracts visual features, tracks identities across frames, derives meaningful real-world events, indexes them into a high-performance vector and relational store, and executes **Temporal RAG** for natural-language Q&A grounded in verifiable video timestamps.

---

## Key Features

- **Adaptive Frame Sampling:** Intelligently skips redundant frames while preserving key temporal dynamics.
- **Detection & Tracking:** YOLO-powered object detection paired with ByteTrack for persistent ID tracking across frames.
- **Attribute Extraction:** Extracts object-level visual metadata (bounding boxes, colors, velocities).
- **Stateful Event Engine:** Detects directional movements, entries, exits, and dwell/stop events.
- **Scene-Level Summarization:** High-level contextual understanding generated via lightweight LLM reasoning.
- **Temporal RAG & Hybrid Retrieval:** Combines structured SQL filters, timestamp windowing, and dense semantic vector search via `pgvector`.
- **Grounded Video Q&A:** Delivers hallucination-resistant answers anchored directly to timestamped evidence sources.
- **Asynchronous Task Queue:** Built on Celery and Redis to handle compute-heavy video ingestion seamlessly.
- **Interactive Dashboard:** React-driven interface for monitoring ingestion progress, exploring event timelines, and querying video data.

---

## System Architecture

```text
                           Video Upload
                                │
                                ▼
                         FastAPI Backend
                                │
                                ▼
                         Celery + Redis
                                │
                                ▼
                    Adaptive Frame Sampling
                                │
                                ▼
                          YOLO Detection
                                │
                                ▼
                       ByteTrack Tracking
                                │
                                ▼
                     Attribute Extraction
                                │
                                ▼
                       Event State Engine
                                │
                   ┌────────────┴────────────┐
                   ▼                         ▼
            Event Database          Scene Understanding
                   │                         │
                   ▼                         ▼
            Event Embeddings            Scene Summary
                   │
                   ▼
          PostgreSQL + pgvector
                   │
                   ▼
          Query Understanding
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
Structured SQL  Temporal      Vector
  Retrieval      Search       Search
     │             │             │
     └─────────────┼─────────────┘
                   │
                   ▼
               LLM / RAG
                   │
                   ▼
            Grounded Answer
                   │
                   ▼
            React Dashboard
```

---

## How It Works

```text
Video Ingestion ──▶ Perception (CV) ──▶ Event Synthesis ──▶ Vector Indexing ──▶ Temporal RAG
```

1. **Video Ingestion & Asynchronous Tasking**  
   Files are uploaded via FastAPI and offloaded to a Celery worker queue backed by Redis, keeping the main HTTP thread non-blocking.
2. **Perception Pipeline (YOLO + ByteTrack)**  
   Frames undergo adaptive sampling. YOLO detects bounding boxes and object classes, while ByteTrack assigns persistent track IDs (`Person #1`, `Vehicle #4`) across occlusions.
3. **Stateful Event Generation**  
   The Event Engine interprets trajectory and state changes over time, converting raw coordinates into semantic occurrences:
   > *"Person #2 entered at 00:12.5, stopped moving at 00:21.5, and exited at 00:30.0."*
4. **Vector Embedding & Indexing**  
   Event strings are vectorized via Sentence Transformers and indexed into PostgreSQL using `pgvector` alongside structured relational metadata.
5. **Dynamic Query Understanding & Grounded Q&A**  
   Queries like *"How many people entered between 10s and 30s?"* are parsed into structured temporal/class constraints and semantic queries, retrieving exact supporting events for LLM generation.

---

## Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend & Pipeline** | Python 3.10+, FastAPI, Celery, Redis, SQLAlchemy |
| **Computer Vision** | YOLO, ByteTrack, OpenCV, NumPy |
| **Embeddings & LLM** | Sentence Transformers, Groq API (Llama 3 / Mixtral) |
| **Database & Search** | PostgreSQL, `pgvector` |
| **Frontend** | React, Tailwind CSS |

---

## Project Structure

```text
sentinel-ai/
├── app/
│   ├── ai/                      # Vector embedding, LLM, and query parsing services
│   │   ├── event_embedder.py
│   │   ├── event_indexer.py
│   │   ├── event_search.py
│   │   ├── llm_service.py
│   │   ├── qa_service.py
│   │   ├── query_understanding.py
│   │   └── scene_understanding.py
│   ├── api/                     # Video upload & management routes
│   │   └── routes_video.py
│   ├── cv/                      # Computer vision pipelines
│   │   ├── attribute_extractor.py
│   │   └── perception.py
│   ├── models/                  # Database schemas & ORM models
│   │   └── schema.py
│   ├── pipeline/                # Video processing & event generation
│   │   ├── event_engine.py
│   │   └── frame_sampler.py
│   ├── routes/                  # Event query & timeline routes
│   │   ├── events.py
│   │   └── query.py
│   ├── celery_app.py
│   ├── config.py
│   ├── database.py
│   ├── init_db.py
│   ├── main.py
│   └── worker.py
├── check_models.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL instance with the `pgvector` extension enabled
- Redis server running locally or accessible remotely

### 1. Clone the Repository

```bash
git clone [https://github.com/raunak5131/sentinel-ai.git](https://github.com/raunak5131/sentinel-ai.git)
cd sentinel-ai
```

### 2. Set Up Virtual Environment

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/sentinel_db
REDIS_URL=redis://localhost:6379/0
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 5. Initialize the Database

```bash
python -m app.init_db
```

---

## Running SentinelAI

Run the following processes in separate terminal instances:

#### 1. Start the API Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Start the Background Celery Worker
```bash
# Windows
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo

# Linux / macOS
celery -A app.celery_app.celery_app worker --loglevel=info
```

---

## API Endpoints

### Ingestion & Video Management

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/videos/upload` | Uploads a video file and dispatches a background task |
| `GET` | `/videos` | Lists all uploaded videos and processing states |
| `GET` | `/videos/{video_id}/status` | Checks background processing status for a video |

### Temporal Querying & Intelligence

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/videos/{video_id}/query` | Submits a natural-language query against the video |

#### Example Query Request

```bash
curl -X POST "http://localhost:8000/videos/vid_8fbc2e1a/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "How many red vehicles stopped near the entrance between 10 and 30 seconds?",
       "limit": 8
     }'
```

#### Example Response

```json
{
  "video_id": "vid_8fbc2e1a",
  "question": "How many red vehicles stopped near the entrance between 10 and 30 seconds?",
  "answer": "One red vehicle (Vehicle #3) was observed coming to a stop at 18.4 seconds near the entrance area.",
  "sources": [
    {
      "track_id": 3,
      "class_name": "car",
      "color": "red",
      "event_type": "stopped",
      "timestamp": 18.4,
      "confidence": 0.94
    }
  ]
}
```

---

## Roadmap

- [ ] Real-time RTSP/CCTV continuous stream processing
- [ ] Multi-camera object re-identification (Re-ID)
- [ ] Visual clip extraction & automated snippet rendering in UI
- [ ] Edge deployment support (NVIDIA Jetson / TensorRT acceleration)
- [ ] Anomaly detection for perimeter breaches and industrial hazards
- [ ] Webhook triggers and automated incident reporting

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
