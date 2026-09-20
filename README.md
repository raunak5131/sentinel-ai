<div align="center">



\# 👁️ SentinelAI



\### AI-Powered Video Intelligence \& Temporal RAG



\[!\[FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge\&logo=fastapi)](https://fastapi.tiangolo.com/)

\[!\[YOLO](https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge\&logo=ultralytics\&logoColor=black)](https://ultralytics.com/)

\[!\[PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge\&logo=pytorch\&logoColor=white)](https://pytorch.org/)

\[!\[PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge\&logo=postgresql\&logoColor=white)](https://www.postgresql.org/)

\[!\[pgvector](https://img.shields.io/badge/pgvector-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)](https://github.com/pgvector/pgvector)

\[!\[Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge\&logo=celery\&logoColor=white)](https://docs.celeryq.dev/)

\[!\[Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge\&logo=redis\&logoColor=white)](https://redis.io/)

\[!\[React](https://img.shields.io/badge/React-20232A?style=for-the-badge\&logo=react\&logoColor=61DAFB)](https://reactjs.org/)



<p align="center">

&#x20; <b>Transform long, dense video feeds into structured, searchable, and explainable intelligence using Computer Vision, Event State Engines, and Temporal RAG.</b>

</p>



\[Key Features](#-key-features) •

\[Architecture](#-system-architecture) •

\[How It Works](#-how-it-works) •

\[Tech Stack](#-technology-stack) •

\[Getting Started](#-getting-started) •

\[API Reference](#-api-endpoints)



</div>



\---



\## 📌 Overview



\*\*SentinelAI\*\* is an end-to-end video intelligence engine built for long surveillance and industrial video feeds. Instead of overwhelming an LLM with massive, raw frame sequences, SentinelAI extracts visual features, tracks identities across frames, derives meaningful real-world events, indexes them into a high-performance vector and relational store, and executes \*\*Temporal RAG\*\* for natural-language Q\&A grounded in verifiable video timestamps.



\---



\## ✨ Key Features



\- \*\*⚡ Adaptive Frame Sampling:\*\* Intelligently skips redundant frames while preserving key temporal dynamics.

\- \*\*🎯 Detection \& Tracking:\*\* YOLO-powered object detection paired with ByteTrack for persistent ID tracking across frames.

\- \*\*🏷️ Attribute Extraction:\*\* Extracts object-level visual metadata (e.g., bounding boxes, colors, velocities).

\- \*\*⏱️ Stateful Event Engine:\*\* Detects directional movements, entries, exits, and dwell/stop events.

\- \*\*🧠 Scene-Level Summarization:\*\* High-level contextual understanding generated via lightweight LLM reasoning.

\- \*\*🔍 Temporal RAG \& Hybrid Retrieval:\*\* Combines structured SQL filters, timestamp windowing, and dense semantic vector search via `pgvector`.

\- \*\*💬 Grounded Video Q\&A:\*\* Delivers hallucination-resistant answers anchored directly to timestamped evidence sources.

\- \*\*⚙️ Asynchronous Task Queue:\*\* Built on Celery and Redis to handle compute-heavy video ingestion seamlessly.

\- \*\*🖥️ Intuitive Dashboard:\*\* React-driven interface for monitoring ingestion progress, exploring event timelines, and querying video data.



\---



\## 📐 System Architecture



```text

&#x20;                          Video Upload

&#x20;                               │

&#x20;                               ▼

&#x20;                        FastAPI Backend

&#x20;                               │

&#x20;                               ▼

&#x20;                        Celery + Redis

&#x20;                               │

&#x20;                               ▼

&#x20;                   Adaptive Frame Sampling

&#x20;                               │

&#x20;                               ▼

&#x20;                         YOLO Detection

&#x20;                               │

&#x20;                               ▼

&#x20;                      ByteTrack Tracking

&#x20;                               │

&#x20;                               ▼

&#x20;                    Attribute Extraction

&#x20;                               │

&#x20;                               ▼

&#x20;                      Event State Engine

&#x20;                               │

&#x20;                  ┌────────────┴────────────┐

&#x20;                  ▼                         ▼

&#x20;           Event Database          Scene Understanding

&#x20;                  │                         │

&#x20;                  ▼                         ▼

&#x20;           Event Embeddings            Scene Summary

&#x20;                  │

&#x20;                  ▼

&#x20;         PostgreSQL + pgvector

&#x20;                  │

&#x20;                  ▼

&#x20;         Query Understanding

&#x20;                  │

&#x20;    ┌─────────────┼─────────────┐

&#x20;    ▼             ▼             ▼

Structured SQL  Temporal      Vector

&#x20; Retrieval      Search       Search

&#x20;    │             │             │

&#x20;    └─────────────┼─────────────┘

&#x20;                  │

&#x20;                  ▼

&#x20;              LLM / RAG

&#x20;                  │

&#x20;                  ▼

&#x20;           Grounded Answer

&#x20;                  │

&#x20;                  ▼

&#x20;           React Dashboard

```



\---



\## 🔬 How It Works



```

Video Ingestion ──▶ Perception (CV) ──▶ Event Synthesis ──▶ Vector Indexing ──▶ Temporal RAG

```



1\. \*\*Video Ingestion \& Asynchronous Tasking\*\*  

&#x20;  Files are uploaded via FastAPI and offloaded to a Celery worker queue backed by Redis, keeping the main HTTP thread non-blocking.

2\. \*\*Perception Pipeline (YOLO + ByteTrack)\*\*  

&#x20;  Frames undergo adaptive sampling. YOLO detects bounding boxes and object classes, while ByteTrack assigns persistent track IDs (`Person #1`, `Vehicle #4`) across occlusions.

3\. \*\*Stateful Event Generation\*\*  

&#x20;  The Event Engine interprets trajectory and state changes over time, converting raw coordinates into semantic occurrences:

&#x20;  > \*"Person #2 entered at 00:12.5, stopped moving at 00:21.5, and exited at 00:30.0."\*

4\. \*\*Vector Embedding \& Indexing\*\*  

&#x20;  Event strings are vectorized via Sentence Transformers and indexed into PostgreSQL using `pgvector` alongside structured relational metadata.

5\. \*\*Dynamic Query Understanding \& Grounded Q\&A\*\*  

&#x20;  Queries like \*"How many people entered between 10s and 30s?"\* are parsed into structured temporal/class constraints and semantic queries, retrieving exact supporting events for LLM generation.



\---



\## 🛠️ Technology Stack



| Layer | Technologies |

| :--- | :--- |

| \*\*Backend \& Pipeline\*\* | Python 3.10+, FastAPI, Celery, Redis, SQLAlchemy |

| \*\*Computer Vision\*\* | YOLO, ByteTrack, OpenCV, NumPy |

| \*\*Embeddings \& LLM\*\* | Sentence Transformers, Groq API (Llama 3 / Mixtral) |

| \*\*Database \& Search\*\* | PostgreSQL, `pgvector` |

| \*\*Frontend\*\* | React, Tailwind CSS |



\---



\## 📂 Project Structure



```text

sentinel-ai/

├── app/

│   ├── ai/                      # Vector embedding, LLM, and query parsing services

│   │   ├── event\_embedder.py

│   │   ├── event\_indexer.py

│   │   ├── event\_search.py

│   │   ├── llm\_service.py

│   │   ├── qa\_service.py

│   │   ├── query\_understanding.py

│   │   └── scene\_understanding.py

│   ├── api/                     # Video upload \& management routes

│   │   └── routes\_video.py

│   ├── cv/                      # Computer vision pipelines

│   │   ├── attribute\_extractor.py

│   │   └── perception.py

│   ├── models/                  # Database schemas \& ORM models

│   │   └── schema.py

│   ├── pipeline/                # Video processing \& event generation

│   │   ├── event\_engine.py

│   │   └── frame\_sampler.py

│   ├── routes/                  # Event query \& timeline routes

│   │   ├── events.py

│   │   └── query.py

│   ├── celery\_app.py

│   ├── config.py

│   ├── database.py

│   ├── init\_db.py

│   ├── main.py

│   └── worker.py

├── check\_models.py

├── requirements.txt

├── .gitignore

└── README.md

```



\---



\## 🚀 Getting Started



\### Prerequisites



\- Python 3.10+

\- PostgreSQL instance with the `pgvector` extension enabled

\- Redis server running locally or accessible remotely



\### 1. Clone the Repository



```bash

git clone \[https://github.com/raunak5131/sentinel-ai.git](https://github.com/raunak5131/sentinel-ai.git)

cd sentinel-ai

```



\### 2. Set Up Virtual Environment



\*\*Linux / macOS:\*\*

```bash

python -m venv venv

source venv/bin/activate

```



\*\*Windows (PowerShell):\*\*

```powershell

python -m venv venv

venv\\Scripts\\Activate.ps1

```



\### 3. Install Dependencies



```bash

pip install --upgrade pip

pip install -r requirements.txt

```



\### 4. Configure Environment Variables



Create a `.env` file in the root directory:



```env

DATABASE\_URL=postgresql://postgres:password@localhost:5432/sentinel\_db

REDIS\_URL=redis://localhost:6379/0

GROQ\_API\_KEY=gsk\_your\_groq\_api\_key\_here

```



> \*\*Warning:\*\* Never commit `.env` containing sensitive credentials to source control.



\### 5. Initialize the Database



```bash

python -m app.init\_db

```



\---



\## ⚡ Running SentinelAI



Run the following processes in separate terminal instances:



\#### 1. Start the API Server

```bash

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```



\#### 2. Start the Background Celery Worker

```bash

\# Windows

celery -A app.celery\_app.celery\_app worker --loglevel=info --pool=solo



\# Linux / macOS

celery -A app.celery\_app.celery\_app worker --loglevel=info

```



\---



\## 📡 API Endpoints



\### Ingestion \& Video Management



| Method | Endpoint | Description |

| :--- | :--- | :--- |

| `POST` | `/videos/upload` | Uploads a video file and dispatches a background task |

| `GET` | `/videos` | Lists all uploaded videos and processing states |

| `GET` | `/videos/{video\_id}/status` | Checks background processing status for a video |



\### Temporal Querying \& Intelligence



| Method | Endpoint | Description |

| :--- | :--- | :--- |

| `POST` | `/videos/{video\_id}/query` | Submits a natural-language query against the video |



\#### Example Query Request



```bash

curl -X POST "http://localhost:8000/videos/vid\_8fbc2e1a/query" \\

&#x20;    -H "Content-Type: application/json" \\

&#x20;    -d '{

&#x20;      "question": "How many red vehicles stopped near the entrance between 10 and 30 seconds?",

&#x20;      "limit": 8

&#x20;    }'

```



\#### Example Response



```json

{

&#x20; "video\_id": "vid\_8fbc2e1a",

&#x20; "question": "How many red vehicles stopped near the entrance between 10 and 30 seconds?",

&#x20; "answer": "One red vehicle (Vehicle #3) was observed coming to a stop at 18.4 seconds near the entrance area.",

&#x20; "sources": \[

&#x20;   {

&#x20;     "track\_id": 3,

&#x20;     "class\_name": "car",

&#x20;     "color": "red",

&#x20;     "event\_type": "stopped",

&#x20;     "timestamp": 18.4,

&#x20;     "confidence": 0.94

&#x20;   }

&#x20; ]

}

```



\---



\## 🔮 Roadmap



\- \[ ] Real-time RTSP/CCTV continuous stream processing

\- \[ ] Multi-camera object re-identification (Re-ID)

\- \[ ] Visual clip extraction \& automated snippet rendering in UI

\- \[ ] Edge deployment support (NVIDIA Jetson / TensorRT acceleration)

\- \[ ] Anomaly detection for perimeter breaches and industrial hazards

\- \[ ] Webhook triggers and automated incident reporting



\---




