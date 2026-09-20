<div align="center">

# 🛰️ SentinelAI

### AI-Powered Video Intelligence & Temporal RAG

*Transform raw surveillance and industrial video into searchable, explainable intelligence.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Async%20Tasks-37814A?logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Broker-DC382D?logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-Dashboard-61DAFB?logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-Personal%20Project-lightgrey)

</div>

---

## 📖 Overview

**SentinelAI** is an AI-powered video intelligence system that analyzes long surveillance and industrial videos, detects and tracks objects, converts visual activity into timestamped events, and enables users to query videos using natural language.

It combines **computer vision**, **event-based reasoning**, **vector search**, **Temporal RAG**, and **LLMs** to turn raw video into searchable and explainable intelligence.

---

## ✨ Features

| Category | Capability |
|---|---|
| 🎞️ Video Processing | Long-video processing with adaptive frame sampling |
| 🎯 Detection | YOLO-based object detection |
| 🧭 Tracking | ByteTrack multi-object tracking with persistent identities |
| 🎨 Attributes | Object attribute extraction (e.g., color) |
| ⏱️ Events | Stateful event detection — entry, exit, movement, stoppage |
| 🧠 Scene AI | AI-powered scene understanding and summarization |
| 🔎 Embeddings | Event embeddings via Sentence Transformers |
| 🗄️ Storage | PostgreSQL + pgvector for vector storage and retrieval |
| 🔗 Retrieval | Temporal RAG for event-grounded video search |
| 💬 Q&A | Natural-language video querying |
| ⚡ Hybrid Search | Structured SQL + semantic vector retrieval |
| 📍 Grounding | Timestamp-grounded answers with event sources |
| ⚙️ Async | Background processing via Celery + Redis |
| 🖥️ Dashboard | React UI for uploads, status, timelines, and querying |

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
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Event Database      Scene Understanding
                    │
                    ▼
              Event Embeddings
                    │
                    ▼
             PostgreSQL + pgvector
                    │
                    ▼
             Query Understanding
                    │
          ┌─────────┼──────────┬─────────┐
          ▼         ▼          ▼
     Structured   Temporal    Vector
      Retrieval    Search     Search
          │         │          │
          └─────────┼──────────┘
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

## ⚙️ How It Works

### 1. Video Processing
Users upload a video through the FastAPI backend. Long-running processing is handled asynchronously using **Celery + Redis**, so the API stays responsive while videos process in the background.

### 2. Adaptive Frame Sampling
Instead of processing every frame, SentinelAI samples frames at a configured rate and uses frame-change information to cut unnecessary work — preserving temporal fidelity on long videos.

### 3. Object Detection
Sampled frames are processed with **YOLO**. Each detection includes:
- Object class
- Bounding box
- Confidence
- Tracking identity

### 4. Multi-Object Tracking
**ByteTrack** associates detections across frames and maintains persistent identities, e.g.:

```text
Person #1
Person #2
Person #3
```

This lets SentinelAI reason about how individual objects behave over time.

### 5. Attribute Extraction
Additional information is extracted from detected objects:

```text
Object: person
Color: blue
```

Stored as event metadata for retrieval and analysis.

### 6. Event Detection
The Event Engine converts tracking data into higher-level temporal events:

```text
Person entered at 12.5 seconds
Person started moving at 15.0 seconds
Person stopped at 21.5 seconds
Person exited at 30.0 seconds
```

Each event carries: timestamp, event type, object class, track identity, confidence, description, and metadata.

### 7. Scene Understanding
Detected objects are summarized into scene-level context using an LLM:

```text
Scene Type: crowd
Objects: person, sports ball
```

### 8. Event Embeddings
Each event becomes a searchable text representation, e.g.:

```text
At 21.5 seconds, person stopped.
```

**Sentence Transformers** generate embeddings, stored in **PostgreSQL + pgvector**.

### 9. Temporal RAG
Rather than feeding an entire video to an LLM, SentinelAI retrieves relevant events using semantic similarity and temporal constraints — answering questions with grounded evidence.

### 10. Natural-Language Query Understanding
Questions are converted into structured retrieval requirements. For example:

```text
"How many people entered?"
→ Intent: count | Object: person | Event: entered
```

```text
"What happened around 20 seconds?"
→ Temporal query around the requested timestamp
```

The system combines **structured SQL filtering**, **timestamp filtering**, and **semantic vector search** as needed. Object classes are determined dynamically from what's detected in the video — not a fixed list.

### 11. Grounded Video Q&A
Retrieved events are passed to the LLM as context. Answers include timestamps tied to evidence, and the system is designed to avoid inventing objects, actions, timestamps, or events not present in the retrieved context.

---

## 💬 Example Queries

```text
How many people entered?
Which vehicles stopped?
What happened around 20 seconds?
What happened between 10 and 15 seconds?
What happened to Person #3?
Which objects exited the scene?
Were there any objects that stopped moving?
What objects were detected in the video?
```

---

## 🧰 Technology Stack

<table>
<tr><td><b>Backend</b></td><td>Python · FastAPI · Celery · Redis · SQLAlchemy</td></tr>
<tr><td><b>Computer Vision</b></td><td>YOLO · ByteTrack · OpenCV · NumPy</td></tr>
<tr><td><b>AI / ML</b></td><td>Sentence Transformers · LLM Scene Understanding · LLM Query Understanding · Temporal RAG</td></tr>
<tr><td><b>Database</b></td><td>PostgreSQL · pgvector</td></tr>
<tr><td><b>Frontend</b></td><td>React</td></tr>
<tr><td><b>LLM Provider</b></td><td>Groq API</td></tr>
</table>

---

## 📁 Project Structure

```text
sentinel-ai/
│
├── app/
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
```

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/raunak5131/sentinel-ai.git
cd sentinel-ai
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

**3. Activate the virtual environment**

Windows Git Bash:
```bash
source venv/Scripts/activate
```

Windows PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_string
REDIS_URL=your_redis_connection_string
GROQ_API_KEY=your_groq_api_key
```

> ⚠️ Do **not** commit `.env` to GitHub. A `.gitignore` is already included to keep environment variables, virtual environments, uploaded videos, model files, and other generated files out of version control.

---

## 🗄️ Database Setup

```bash
python -m app.init_db
```

Make sure PostgreSQL and pgvector are available before starting video processing.

---

## ▶️ Running the Application

**Start the FastAPI server**
```bash
uvicorn app.main:app --reload
```

**Start the Celery worker**
```bash
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo
```

> Celery worker configuration may vary by OS and deployment environment.

---

## 🔌 API Endpoints

### Upload Video
```http
POST /videos/upload
```
Uploads a video and starts asynchronous processing.

### List Videos
```http
GET /videos
```
Returns available videos and their processing status.

### Video Status
```http
GET /videos/{video_id}/status
```
Returns the current processing status of a video.

### Query Video
```http
POST /videos/{video_id}/query
```

**Request**
```json
{
    "question": "How many people entered?",
    "limit": 8
}
```

**Response**
```json
{
    "video_id": "video-id",
    "question": "How many people entered?",
    "answer": "Five people entered the scene.",
    "sources": []
}
```

---

## 🔄 Processing Pipeline

```text
Upload → Video Record Created → Celery Background Task
       → Frame Sampling → Object Detection → Object Tracking
       → Attribute Extraction → Event Generation → Event Storage
       → Event Embedding → Vector Indexing → Scene Understanding
       → Video Summary → Ready for Q&A
```

## 🔍 Query Pipeline

```text
User Question → Query Understanding
             → [ Structured / Temporal / Semantic Retrieval ]
             → Relevant Events → Context Construction
             → LLM → Grounded Answer + Sources
```

---

## 🎯 Design Goals

- **Event-Centric Video Understanding** — video is treated as structured temporal events, not just independent frames.
- **Grounded AI Responses** — the LLM answers using retrieved event evidence, not guesswork.
- **Scalable Processing** — async tasks, frame sampling, tracking, and vector retrieval support longer videos.
- **Dynamic Querying** — object classes come from what's actually in the video, not a fixed predefined list.

---

## 🔮 Future Scope

- Real-time CCTV stream processing
- Multi-camera video intelligence
- Advanced anomaly detection
- Cross-video event search
- Person and object re-identification
- Advanced temporal reasoning
- Natural-language video clip retrieval
- Real-time alerts and notifications
- Industrial safety monitoring
- Automated incident reporting

---

## 🌟 Project Highlights

```text
Computer Vision + Object Tracking + Event-Based Reasoning
+ Vector Search + Temporal RAG + LLM Reasoning
+ Asynchronous Processing + Web Dashboard
```

The goal: transform raw video into structured, searchable, and explainable information.

---

<div align="center">

**[⭐ Star this repo](https://github.com/raunak5131/sentinel-ai)** if you find it useful!

</div>
