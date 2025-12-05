🚀 Multi-Agent GenAI Platform
<p align="center"> <img src="docs/architecture.png" width="75%" alt="Architecture Diagram (Add PNG Here)" /> </p> <p align="center"> <b>Autonomous Research • LLM Reasoning • Vector Search • PPT + Video Generation • Cloud-Native Orchestration</b> </p> <p align="center"> A production-grade, multi-agent generative AI system inspired by engineering patterns used at Google, Meta, Amazon, Microsoft, NVIDIA and OpenAI. </p>
🔰 Table of Contents
Overview

Architecture

Features

Tech Stack

How It Works

Project Structure

Developer Setup

Environment Variables

API Documentation

Docker & Kubernetes

CI/CD

Observability

Demo

Contributing

License

Contact

📌 Overview
The Multi-Agent GenAI Platform is an autonomous research and knowledge-generation system that can:

Retrieve scientific and technical information

Perform structured LLM reasoning

Generate PPT slides and narrated videos

Index all knowledge using vector search

Run distributed pipelines using Celery

Provide full observability, tracing, dashboards, and logs

Deploy to Kubernetes using Helm

Run real-world CI/CD (GitHub Actions → Docker → K8s)

This project is designed for:

FAANG-level portfolio showcase

Enterprise AI architecture demonstrations

Research automation

Cloud-native distributed systems practice

🏗 Architecture
✔ Multi-agent orchestration
✔ Async FastAPI backend
✔ Distributed Celery workers
✔ Vector search ingestion pipeline
✔ Media generation pipeline
✔ Observability stack

Replace docs/architecture.png with your architecture PNG.

🧠 Features
Multi-Agent AI System
Agent	Responsibility
SearchAgent	Scientific paper retrieval + web queries
SummarizerAgent	LLM-based structured summarization
IngestAgent	Embedding generation + Pinecone indexing
MediaAgent	PPT creation + narrated video generation

Distributed Processing
FastAPI async backend

Celery workers (parallel research + ingestion + media)

Redis/RabbitMQ message broker

Task state tracked in Postgres

Media Generation
PPT creation (python-pptx)

AI narrations (gTTS)

Video synthesis (MoviePy + ffmpeg)

Semantic Search
SentenceTransformers embeddings

Pinecone vector database

Local SQLite fallback

Observability
Prometheus metrics

Grafana dashboards

OpenTelemetry distributed tracing

JSON structured logs

Security
OAuth2 + JWT authentication

Rate limiting

Sentry error tracking

Kubernetes PodSecurity + NetworkPolicies

⚙️ Tech Stack
Layer	Technologies
Frontend	Next.js, React, Tailwind
Backend	FastAPI, Celery, SQLModel
AI/ML	OpenAI/Local LLMs, SentenceTransformers, Pinecone
Workers	Celery, MoviePy, gTTS
Database	Postgres, Redis
Infra	Docker, Kubernetes, Helm
Observability	Prometheus, Grafana, OpenTelemetry
CI/CD	GitHub Actions

📁 Project Structure
bash
Copy code
multi-agent-genai-platform/
│
├── backend/
│   ├── api/             # FastAPI backend
│   ├── workers/         # Celery workers
│   └── requirements.txt
│
├── frontend/
│   └── nextjs-app/      # Next.js dashboard
│
├── infra/
│   ├── docker-compose.yml
│   ├── helm-chart/
│   └── k8s/
│
├── docs/
│   ├── architecture.png
│   └── demo/
│        └── demo.gif
│
└── grafana/
    ├── dashboard_full.json
    ├── dashboard_enterprise.json
🧪 Developer Setup
Clone repository
bash
Copy code
git clone https://github.com/rathishbarath/multi-agent-genai-platform
cd multi-agent-genai-platform
🔧 Backend Setup
bash
Copy code
cd backend/api
pip install -r requirements.txt
uvicorn main:app --reload
🔧 Worker Setup
bash
Copy code
cd backend/workers
pip install -r ../api/requirements.txt
celery -A api.workers.celery_app.celery_app worker --loglevel=info
🎨 Frontend Setup
bash
Copy code
cd frontend/nextjs-app
npm install
npm run dev
🐳 Docker (Full Stack)
bash
Copy code
cd infra
docker-compose up --build
🔐 Environment Variables
Create backend/api/.env:

ini
Copy code
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/autoscillab
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:postgres@localhost:5432/autoscillab

REDIS_URL=redis://localhost:6379/0

JWT_SECRET=change_me
LLM_API_KEY=
PINECONE_API_KEY=
SENTRY_DSN=
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
📘 API Documentation
Start Research Pipeline
http
Copy code
POST /agents/start_research
Request
json
Copy code
{
  "query": "LLM optimization techniques"
}
Response
json
Copy code
{
  "task_id": "f392bc3e-1b7d-4633-bb14-3a10d9c9adac",
  "status": "queued"
}
Check Task Status
http
Copy code
GET /agents/task_status/{task_id}
Semantic Search
http
Copy code
GET /research/search?q=...
☸️ Docker & Kubernetes
Includes:

Dockerfiles (backend, workers, frontend)

docker-compose orchestrator

Helm chart for Kubernetes deployment

K8s manifests for:

Deployment

Service

Ingress

HPA

NetworkPolicies

🚦 CI/CD
GitHub Actions Pipelines:

Pipeline	Function
ci.yaml	Build + Lint + Test
e2e-celery.yml	Full pipeline run (search → summarize → ingest → media)
cd.yaml	Docker build → Push → Kubernetes deploy

Required GitHub Secrets:

nginx
Copy code
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
KUBE_CONFIG_DATA
JWT_SECRET
LLM_API_KEY
PINECONE_API_KEY
📊 Observability
Metrics
bash
Copy code
/metrics
Dashboards
Import:

grafana/dashboard_full.json

grafana/dashboard_enterprise.json

Tracing
Enabled for:

FastAPI routes

Celery tasks

DB operations

🎥 Demo
Add your GIF here:

md
Copy code
<p align="center">
  <img src="docs/demo/demo.gif" width="70%" />
</p>
🤝 Contributing
Follow Conventional Commits:

vbnet
Copy code
feat: add summarization pipeline
fix: celery reconnect logic
docs: update architecture diagram
refactor: async ingestion workflow
Pull Requests welcome!

📄 License
Distributed under the Apache 2.0 License.
See LICENSE for details.

📬 Contact
Rathish Barath
GitHub: https://github.com/rathishbarath
Email: your_email@example.com (replace)
