<!-- PROJECT BANNER -->
<p align="center">
  <img src="docs/images/banner.png" width="100%" />
</p>

# 🚀 Multi-Agent GenAI Platform  
**Autonomous Research • LLM Reasoning • Vector Search • PPT & Video Generation • Cloud-Native Architecture**

---

<p align="center">
  <!-- Build Badges -->
  <a href="https://github.com/Rathishbarath/multi-agent-genai-platform/actions/workflows/ci.yaml">
    <img src="https://github.com/Rathishbarath/multi-agent-genai-platform/actions/workflows/ci.yaml/badge.svg" />
  </a>
  <a href="https://github.com/Rathishbarath/multi-agent-genai-platform/actions/workflows/e2e-celery.yml">
    <img src="https://github.com/Rathishbarath/multi-agent-genai-platform/actions/workflows/e2e-celery.yml/badge.svg" />
  </a>
  <a href="https://github.com/Rathishbarath/multi-agent-genai-platform/actions/workflows/cd.yaml">
    <img src="https://github.com/Rathishbarath/multi-agent-genai-platform/actions/workflows/cd.yaml/badge.svg" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.10_|_3.11-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Production--Ready-teal" />
  <img src="https://img.shields.io/badge/Next.js-Frontend-black" />
  <img src="https://img.shields.io/badge/Kubernetes-Ready-blue" />
  <img src="https://img.shields.io/badge/License-Apache_2.0-green" />
</p>

---

# 📌 Overview
A fully **production-grade multi-agent GenAI orchestration platform** designed following engineering patterns used at:

**Google · Meta · Amazon · Microsoft · Intuit · NVIDIA · OpenAI**

The system autonomously:

- Retrieves scientific research  
- Performs LLM reasoning + structured summarization  
- Generates PPT slides & narrated videos  
- Indexes and searches knowledge via Pinecone  
- Runs distributed background pipelines (Celery + Redis/RabbitMQ)  
- Provides observability (Prometheus, Grafana, OpenTelemetry)  
- Deploys via Kubernetes + Helm  
- Runs full CI/CD pipelines with GitHub Actions  

Perfect for **FAANG interviews, enterprise projects, architecture discussions, and portfolio showcase**.

---

# 🏗 Architecture (PNG)

<p align="center">
  <img src="docs/images/architecture.png" width="95%" />
</p>

---

# 🧠 Features

### Multi-Agent AI System
- **SearchAgent** → scientific paper retrieval  
- **SummarizerAgent** → structured LLM summarization  
- **IngestAgent** → embeddings + Pinecone index  
- **MediaAgent** → PPT & narrated video generation  

### Distributed Processing
- FastAPI async backend  
- Celery workers  
- Redis/RabbitMQ message broker  
- Task status tracked in Postgres  

### Media Generation
- PPT creation (`python-pptx`)  
- AI-narrated videos (MoviePy + gTTS + ffmpeg)  

### Semantic Search
- SentenceTransformers embeddings  
- Pinecone vector database  
- SQLite fallback for local mode  

### Observability
- Prometheus metrics  
- Grafana dashboards  
- OpenTelemetry distributed tracing  
- JSON-structured logging  

### Security
- OAuth2 / JWT  
- Rate limiting  
- Sentry error tracking  
- Kubernetes PodSecurity + NetworkPolicies  

---

# ⚙️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Next.js, React, Tailwind |
| **Backend** | FastAPI, Celery, SQLModel, Redis, Postgres |
| **ML/AI** | LLM (OpenAI / Local), SentenceTransformers, Pinecone |
| **Workers** | Celery, MoviePy, gTTS |
| **DB / Cache** | Postgres, Redis |
| **Infra** | Docker, Kubernetes, Helm |
| **Observability** | Prometheus, Grafana, OpenTelemetry |
| **CI/CD** | GitHub Actions |

---

# 🧪 Developer Quickstart

## Clone repository
```bash
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
🚦 CI/CD Pipelines
✔ ci.yaml — Build + Test + Lint
✔ e2e-celery.yml — Full research → summarize → ingest → media test
✔ cd.yaml — Docker Build → Push → Kubernetes Deploy
Required GitHub Secrets
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
Import from:

bash
Copy code
grafana/dashboard_full.json
grafana/dashboard_enterprise.json
Tracing
Enabled via OTEL for:

FastAPI routes

Celery tasks

Database operations

📘 API Documentation
Start Research Pipeline
POST /agents/start_research

json
Copy code
{ "query": "LLM optimization techniques" }
Check Task Status
GET /agents/task_status/{task_id}

Semantic Search
GET /research/search?q=...

🎥 Demo (GIF)
Generate GIF:

bash
Copy code
bash scripts/generate_demo_gif.sh
Display in README:

<p align="center"> <img src="docs/demo/demo.gif" width="70%" /> </p>
🌍 Portfolio Section (For your website)
Copy this section to your portfolio website.

🌟 Multi-Agent GenAI Platform
A production-grade orchestration system capable of autonomous research, LLM reasoning, vector search, PPT creation, and narrated video generation — powered by distributed microservices and cloud-native infrastructure.

Highlights

Multi-agent reasoning

Automatic media generation

Semantic search

Kubernetes-native

Prometheus + Grafana observability

Production-level architecture

GitHub:
👉 https://github.com/rathishbarath/multi-agent-genai-platform

🔎 SEO Keywords (Paste into GitHub Topics)
sql
Copy code
genai, multi-agent-system, llm, robotics, orchestration, automation,
vector-search, pinecone, fastapi, nextjs, ai-platform, distributed-systems,
celery, kubernetes, helm, opentelemetry, grafana, prometheus, research-automation,
semantic-search, python, react, cloud-native
🤝 Contributing Guidelines
Follow Conventional Commits:

vbnet
Copy code
feat: add summarizer agent
fix: redis reconnect logic
docs: improve architecture diagram
refactor: orchestrator async pipeline
📄 License
Apache 2.0

📬 Contact
Rathish Barath
GitHub: https://github.com/rathishbarath
Email: your_email@example.com
