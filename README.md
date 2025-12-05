
![Uploading ChatGPT Image Dec 5, 2025, 08_05_56 PM.png…]()

# 🚀 Multi-Agent GenAI Platform  
**Autonomous Research • LLM Reasoning • Vector Search • PPT & Video Generation • Cloud-Native Architecture**

<p align="center">
  <a href="https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/ci.yaml">
    <img src="https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/ci.yaml/badge.svg" />
  </a>
  <a href="https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/e2e-celery.yml">
    <img src="https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/e2e-celery.yml/badge.svg" />
  </a>
  <a href="https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/cd.yaml">
    <img src="https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/cd.yaml/badge.svg" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.10_|_3.11-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal" />
  <img src="https://img.shields.io/badge/Next.js-Frontend-black" />
  <img src="https://img.shields.io/badge/Kubernetes-Ready-blue" />
  <img src="https://img.shields.io/badge/License-Apache_2.0-green" />
</p>

---

# 📌 Overview

This is a **production-grade Multi-Agent GenAI Orchestration Platform** built using real enterprise architecture patterns used inside:


The system autonomously:

- Retrieves research papers (Semantic Scholar + arXiv)  
- Performs structured LLM reasoning  
- Generates vector embeddings  
- Indexes knowledge in Pinecone  
- Produces PPT slides + narrated videos  
- Runs distributed pipelines using Celery  
- Exposes a modern Next.js frontend  
- Ships with full observability (Prometheus, Grafana, OTEL)  
- Deploys to Kubernetes via Helm + GitHub Actions CD  



# 🏗 Architecture Diagram (PNG)


<img width="1536" height="1024" alt="ChatGPT Image Dec 5, 2025, 08_00_44 PM" src="https://github.com/user-attachments/assets/482aee61-232d-402c-8698-593d1ac7a8a2" />

---

# 🧱 End-to-End System Architecture

### **Frontend Layer (Next.js 14)**
- User dashboard  
- Task status  
- Trigger workflows  
- Proxy layer to backend  
- Secure SSR support  

### **Backend Layer (FastAPI)**
- Auth (JWT / OAuth2)  
- Research orchestration  
- LLM summarization  
- Embeddings + Vector Search  
- PPT + Video endpoints  
- Health, metrics, tracing  

### **Worker Layer (Celery)**
Handles long-running async jobs:
- Research orchestration  
- Summarization  
- Vector ingestion  
- PPT generation  
- Video generation  

### **ML & Storage Layer**
- Pinecone vector database  
- Redis cache  
- Postgres database  
- Optional MinIO/S3 for media  

### **DevOps & Observability**
- Prometheus (metrics)  
- Grafana (dashboards)  
- Sentry (errors)  
- OpenTelemetry (traces)  
- Kubernetes + Helm  
- GitHub Actions CI/CD  

---

# 🌟 Features

### 🧠 Multi-Agent AI
- SearchAgent  
- SummarizerAgent  
- EmbeddingsAgent  
- MediaAgent (PPT/Video)  

### ⚡ Distributed Pipeline
- Async FastAPI  
- Celery workers  
- Redis/RabbitMQ broker  

### 🎥 Media Generation
- PPT via python-pptx  
- Narrated video via MoviePy + gTTS  

### 🔍 Semantic Search
- SentenceTransformers embeddings  
- Pinecone indexing  
- SQLite fallback  

### 📈 Observability
- `/metrics` endpoint  
- OTEL traces  
- Grafana dashboards  

### 🔒 Security
- JWT Auth  
- Rate limiting  
- PodSecurity & NetworkPolicies  
- Sentry logging  

---

# ⚙️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Next.js, React, Tailwind |
| **Backend** | FastAPI, SQLModel, Celery, Redis |
| **Vector Search** | Pinecone, SentenceTransformers |
| **Workers** | Celery, MoviePy, python-pptx |
| **Database** | Postgres |
| **Infra** | Docker, Kubernetes, Helm |
| **Observability** | Prometheus, Grafana, OTEL |
| **CI/CD** | GitHub Actions, DockerHub |

---

# 🧪 Developer Quickstart

## Clone the repository
```bash
git clone https://github.com/rathishbarath/multi-agent-genai-platform
cd multi-agent-genai-platform
🔧 Backend Setup
bash
Copy code
cd backend/api
pip install -r requirements.txt
uvicorn main:app --reload
🚀 Start Celery Worker
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
🐳 Full-stack via Docker
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
🏭 Database & Migrations
bash
Copy code
cd backend/api
alembic upgrade head
🔁 CI/CD Pipelines
✔ CI
Tests, linting, build

✔ E2E Celery Tests
Runs full research → summarize → ingest → media pipeline

✔ CD Deployment
Docker build

DockerHub push

Helm deployment to Kubernetes

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
Prometheus
Metrics exposed at:

bash
Copy code
/metrics
Grafana
Dashboards located at:

bash
Copy code
grafana/dashboard_full.json
grafana/dashboard_enterprise.json
OpenTelemetry
Traces emitted by:

FastAPI routes

Celery operations

LLM calls

📘 API Documentation (Summary)
POST /agents/start_research
Triggers full research pipeline.

json
Copy code
{ "query": "LLM optimization techniques" }
GET /agents/task_status/{task_id}
Fetches:

Summary

PPT URL

Video URL

Status

GET /research/search?q=...
Semantic research lookup.

🎥 Demo GIF
Generate:

bash
Copy code
bash scripts/generate_demo_gif.sh
Embed:


Multi-Agent GenAI Platform

A production-ready AI orchestration engine built with distributed microservices, LLM reasoning, semantic search, and automated media generation.

🔗 GitHub: https://github.com/rathishbarath/multi-agent-genai-platform

🔎 SEO Keywords (GitHub Topics)
sql
Copy code
genai, multi-agent, vector-search, fastapi, nextjs, llm, pinecone,
orchestration, research-automation, semantic-search, celery, kubernetes,
helm, opentelemetry, grafana, prometheus, moviepy, python-pptx,
distributed-systems, cloud-native
🤝 Contributing
Follow Conventional Commits:

vbnet
Copy code
feat: add summarizer agent
fix: redis reconnect logic
docs: improve architecture diagram
refactor: orchestrator async improvements
📄 License
Apache 2.0

📬 Contact
Rathish Barath
GitHub: https://github.com/rathishbarath
Email: your_email@example.com
