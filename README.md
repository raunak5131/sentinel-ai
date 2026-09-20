<h1 align="center">👁️ SentinelAI</h1>

<p align="center">
  <strong>AI-Powered Video Intelligence & Temporal RAG</strong>
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  </a>
  <a href="https://www.ultralytics.com/">
    <img src="https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge&logo=ultralytics&logoColor=black" alt="YOLO">
  </a>
  <a href="https://pytorch.org/">
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://github.com/pgvector/pgvector">
    <img src="https://img.shields.io/badge/pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="pgvector">
  </a>
  <a href="https://docs.celeryq.dev/">
    <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  </a>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis" alt="Redis">
  </a>
  <a href="https://react.dev/">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  </a>
</p>

<p align="center">
  Transform long, dense video feeds into structured, searchable, and explainable intelligence using Computer Vision, Event State Engines, Vector Search, and Temporal RAG.
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#system-architecture">Architecture</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#technology-stack">Tech Stack</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#api-reference">API</a>
</p>

---

## 🚀 Overview

**SentinelAI** is an end-to-end video intelligence system designed to analyze long surveillance and industrial video feeds.

Instead of sending large amounts of raw video directly to an LLM, SentinelAI converts video into structured temporal events using computer vision and object tracking. These events are stored, embedded, indexed, and retrieved through a combination of relational filtering, temporal search, and semantic vector search.

The retrieved evidence is then provided to an LLM to generate **grounded, timestamp-aware answers** to natural-language questions about the video.

---

## ✨ Key Features

- 🎞️ **Adaptive Frame Sampling** — Reduces redundant frame processing while preserving important temporal information.
- 🎯 **Object Detection** — YOLO-based detection of objects and their bounding boxes.
- 🧭 **Multi-Object Tracking** — ByteTrack-based persistent tracking identities across frames.
- 🎨 **Attribute Extraction** — Extracts object-level attributes such as color.
- ⚙️ **Stateful Event Engine** — Converts object trajectories into events such as entry, exit, movement, and stoppage.
- 🧠 **Scene Understanding** — Generates high-level scene descriptions and classifications using an LLM.
- 🔎 **Temporal RAG** — Retrieves relevant events using timestamps and semantic similarity.
- 🗃️ **Vector Search** — Sentence Transformer embeddings stored using PostgreSQL and pgvector.
- 💬 **Natural-Language Video Q&A** — Ask questions about events occurring inside the video.
- 🔀 **Hybrid Retrieval** — Combines structured SQL filtering, temporal constraints, and semantic vector search.
- 🛡️ **Grounded Responses** — LLM responses are generated from retrieved video evidence.
- ⚡ **Asynchronous Processing** — Celery and Redis handle long-running video processing tasks.
- 📊 **Interactive Dashboard** — React interface for video uploads, processing status, event timelines, and video querying.

---

## 🏗️ System Architecture

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
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
             Event Database              Scene Understanding
                    │                             │
                    ▼                             ▼
             Event Embeddings              Scene Summary
                    │
                    ▼
             PostgreSQL + pgvector
                    │
                    ▼
             Query Understanding
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
      Structured  Temporal   Semantic
         SQL       Search    Vector Search
          │         │         │
          └─────────┼─────────┘
                    │
                    ▼
                 LLM / RAG
                    │
                    ▼
             Grounded Answer
                    │
                    ▼
             React Dashboard
🔄 How It Works
1. Video Ingestion

A video is uploaded through the FastAPI backend and stored for asynchronous processing.

Long-running processing tasks are delegated to Celery workers through Redis.

2. Adaptive Frame Sampling

Instead of processing every frame, SentinelAI samples frames at a configured rate and evaluates frame changes to reduce redundant processing.

Raw Video
   │
   ├── Frame 1
   ├── Frame 2
   ├── Frame 3
   ├── ...
   └── Frame N
          │
          ▼
   Adaptive Sampling
          │
          ▼
   Relevant Frames
3. Object Detection & Tracking

YOLO detects objects in sampled frames while ByteTrack associates detections across frames and maintains persistent track identities.

Example:

Person #1
Person #2
Person #3

These identities allow the system to reason about object behavior over time.

4. Attribute Extraction

Detected objects can be enriched with additional visual attributes.

Example:

Object: person
Color: blue
Bounding Box: (x1, y1, x2, y2)
5. Event State Engine

The Event Engine converts object tracks into higher-level temporal events.

Examples:

Person #1 entered at 12.5s
Person #1 started moving at 15.0s
Person #1 stopped at 21.5s
Person #1 exited at 30.0s

Each event stores information such as:

Timestamp
Event type
Object class
Entity / track identity
Confidence
Description
Metadata
6. Event Embedding & Indexing

Events are converted into searchable text representations.

Example:

At 21.5 seconds, person stopped.

Sentence Transformers generate embeddings for these events.

The embeddings and event metadata are stored in PostgreSQL with pgvector.

7. Query Understanding

Natural-language questions are converted into structured retrieval requirements.

Example:

Question:
"How many people entered?"

can be interpreted as:

Intent: count
Object: person
Event: entered

Another example:

Question:
"What happened around 20 seconds?"

can be interpreted as a temporal query around the requested timestamp.

The system dynamically uses object classes present in the selected video rather than relying on a fixed predefined object list.

8. Hybrid Retrieval

Depending on the question, SentinelAI can combine:

Structured SQL Filtering
          +
Temporal Filtering
          +
Semantic Vector Search

This allows both precise queries and more open-ended semantic questions.

9. Grounded Video Q&A

Retrieved events are passed to the LLM as context.

The LLM generates an answer based only on the available event evidence and can provide relevant timestamps.

User Question
      │
      ▼
Query Understanding
      │
      ▼
Relevant Events
      │
      ▼
LLM Context
      │
      ▼
Grounded Answer
🧠 Temporal RAG

SentinelAI uses an event-centric retrieval approach rather than passing an entire video directly to an LLM.

Raw Video
   │
   ▼
Computer Vision
   │
   ▼
Structured Events
   │
   ▼
Event Embeddings
   │
   ▼
PostgreSQL + pgvector
   │
   ▼
Relevant Event Retrieval
   │
   ▼
LLM
   │
   ▼
Timestamp-Grounded Answer

This allows the system to connect natural-language questions with specific events occurring at specific points in the video.

🛠️ Technology Stack
Layer	Technologies
Backend	Python, FastAPI
Task Processing	Celery, Redis
Computer Vision	YOLO, ByteTrack, OpenCV, NumPy
AI / ML	Sentence Transformers, LLMs
RAG	Temporal RAG, Vector Search
Database	PostgreSQL, pgvector, SQLAlchemy
LLM Provider	Groq API
Frontend	React
API	REST
📁 Project Structure
sentinel-ai/
│
├── app/
│   │
│   ├── ai/
│   │   ├── event_embedder.py
│   │   ├── event_indexer.py
│   │   ├── event_search.py
│   │   ├── llm_service.py
│   │   ├── qa_service.py
│   │   ├── query_understanding.py
│   │   └── scene_understanding.py
│   │
│   ├── api/
│   │   └── routes_video.py
│   │
│   ├── cv/
│   │   ├── attribute_extractor.py
│   │   └── perception.py
│   │
│   ├── models/
│   │   └── schema.py
│   │
│   ├── pipeline/
│   │   ├── event_engine.py
│   │   └── frame_sampler.py
│   │
│   ├── routes/
│   │   ├── events.py
│   │   └── query.py
│   │
│   ├── celery_app.py
│   ├── config.py
│   ├── database.py
│   ├── init_db.py
│   ├── main.py
│   └── worker.py
│
├── check_models.py
├── requirements.txt
├── .gitignore
└── README.md
⚡ Getting Started
Prerequisites
Python 3.10+
PostgreSQL with pgvector
Redis
Git
A Groq API key
1. Clone the Repository
git clone https://github.com/raunak5131/sentinel-ai.git
cd sentinel-ai
2. Create Virtual Environment
Windows
python -m venv venv

Git Bash:

source venv/Scripts/activate

PowerShell:

venv\Scripts\Activate.ps1
Linux / macOS
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the project root:

DATABASE_URL=your_postgresql_connection_string
REDIS_URL=your_redis_connection_string
GROQ_API_KEY=your_groq_api_key

⚠️ Never commit .env or expose API keys publicly.

5. Initialize the Database
python -m app.init_db
▶️ Running SentinelAI

Run the API server:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

In another terminal, start the Celery worker.

Windows
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo
Linux / macOS
celery -A app.celery_app.celery_app worker --loglevel=info

The API will be available at:

http://localhost:8000

FastAPI interactive documentation:

http://localhost:8000/docs
🔌 API Reference
Video Upload
POST /videos/upload

Uploads a video and starts asynchronous processing.

List Videos
GET /videos

Returns available videos and their processing states.

Video Status
GET /videos/{video_id}/status

Returns the processing status of a video.

Video Q&A
POST /videos/{video_id}/query

Example request:

{
  "question": "How many people entered?",
  "limit": 8
}

Example response:

{
  "video_id": "video-id",
  "question": "How many people entered?",
  "answer": "Five people entered the scene.",
  "sources": []
}
💬 Example Queries
How many people entered?

Which vehicles stopped?

What happened around 20 seconds?

What happened between 10 and 15 seconds?

What happened to Person #3?

Which objects exited the scene?

Were there any objects that stopped moving?

What objects were detected in the video?
📊 Processing Pipeline
Video Upload
     │
     ▼
FastAPI
     │
     ▼
Celery Worker
     │
     ▼
Frame Sampling
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
Event Generation
     │
     ▼
PostgreSQL
     │
     ▼
Event Embeddings
     │
     ▼
pgvector Index
     │
     ▼
Video Ready for Q&A
🔎 Query Pipeline
                User Question
                      │
                      ▼
             Query Understanding
                      │
           ┌──────────┼──────────┐
           │          │          │
           ▼          ▼          ▼
       Structured   Temporal   Semantic
          SQL        Search     Search
           │          │          │
           └──────────┼──────────┘
                      │
                      ▼
                Event Context
                      │
                      ▼
                     LLM
                      │
                      ▼
             Grounded Answer
                      │
                      ▼
                React UI
🎯 Design Goals
Event-Centric Understanding

Convert raw video frames into structured temporal events that can be stored, searched, and reasoned about.

Grounded AI

Provide the LLM with retrieved event evidence instead of asking it to freely infer what happened in the video.

Efficient Processing

Use adaptive frame sampling and asynchronous task processing to reduce unnecessary computation for long videos.

Hybrid Retrieval

Combine relational database queries, timestamp filtering, and vector similarity search to handle different types of natural-language questions.

Dynamic Querying

Use the objects and events actually detected in a video rather than relying on a fixed predefined object vocabulary.

🚀 Future Scope
 Real-time RTSP / CCTV stream processing
 Multi-camera video intelligence
 Person and object re-identification
 Advanced anomaly detection
 Natural-language video clip retrieval
 Automated incident reporting
 Real-time alerts and notifications
 Edge deployment with GPU acceleration
 Cross-video event search
📌 Project Highlights
Computer Vision
       +
Object Tracking
       +
Event-Based Reasoning
       +
Vector Search
       +
Temporal RAG
       +
LLM Reasoning
       +
Asynchronous Processing
       +
Interactive Dashboard

SentinelAI brings these components together into a single pipeline for turning raw video into structured, searchable, and explainable intelligence.
