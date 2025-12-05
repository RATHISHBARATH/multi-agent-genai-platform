🚀 Multi-Agent GenAI Platform



<img width="1024" height="1024" alt="ChatGPT Image Dec 5, 2025, 07_31_55 PM" src="https://github.com/user-attachments/assets/6c4cf432-fce8-46a4-b349-5a48e849e7f7" />

Autonomous Research • LLM Reasoning • Vector Search • PPT + Video Generation • Cloud-Native Orchestration

<p> A production-grade, distributed generative AI system capable of autonomous deep research, multi-modal content generation, and scalable knowledge retrieval. Designed with patterns inspired by engineering teams at <b>Google, Meta, and OpenAI</b>. </p>

View Demo • Read Docs • Report Bug • Request Feature

</div>

🔰 Table of Contents
📌 Overview

🏗 Architecture

🧠 Key Features

⚙️ Tech Stack

🧪 Developer Setup

🐳 Docker & Deployment

🔐 Environment Variables

📘 API Documentation

📊 Observability

🤝 Contributing

📄 License

📌 Overview
The Multi-Agent GenAI Platform is an event-driven system where specialized AI agents collaborate to solve complex tasks. Unlike simple chatbot wrappers, this platform employs a Map-Reduce pattern for research and a Director-Actor pattern for media generation.

Capabilities
Autonomous Research: Spawns "Researcher Agents" to crawl the web, summarize papers, and validate sources.

RAG at Scale: Ingests enterprise data into vector stores for millisecond-latency semantic retrieval.

Multi-Modal Output: Automatically generates slide decks (PPTX) and synthesizes explanatory videos with AI voiceovers based on research findings.

Target Audience: Enterprise Engineering Teams, Research Labs, and AI Startups requiring scalable agent orchestration.

🏗 Architecture
The system follows a Microservices architecture orchestrated by Kubernetes (or Docker Compose for local dev).

Core Pattern: The backend uses an asynchronous Task Queue pattern. API requests offload heavy compute (LLM inference, video rendering) to background workers.

Orchestrator: FastAPI Gateway handles auth, rate-limiting, and request routing.

Brain (LLM): Configurable backend supporting OpenAI GPT-4, Anthropic Claude, or local Llama 3 via vLLM.

Vector Engine: Asynchronous ingestion pipeline using LangChain and Pinecone/Qdrant.

Media Pipeline: FFmpeg and Python-pptx workers for rendering final assets.

🧠 Features
Multi-Agent AI System
Chain-of-Thought Reasoning: Agents break down complex user queries into sub-tasks (e.g., "Research", "Outline", "Draft").

Self-Correction: A "Critic Agent" reviews outputs for hallucinations before final delivery.

Distributed Processing
Celery + Redis: Robust task queues manage long-running jobs (e.g., video rendering).

Horizontal Scaling: Worker nodes scale independently based on CPU/GPU load.

Media Generation
Dynamic PPTX: text-to-presentation engine with auto-layout and image injection.

Video Synthesis: Text-to-Speech (ElevenLabs/OpenAI) + image transitions synced to audio timestamps.

Observability & Security
OTEL Tracing: Full distributed tracing across microservices.

RBAC: Role-Based Access Control for API endpoints.

⚙️ Tech Stack
Component	Technology	Description
Backend	Python, FastAPI	High-performance Async I/O API
Orchestration	Celery, Redis	Distributed task queue & message broker
AI Framework	LangChain, LlamaIndex	Agentic workflows and RAG
Vector DB	Qdrant / Pinecone	Semantic search engine
Frontend	React, TypeScript, Tailwind	Interactive dashboard for task management
Infrastructure	Docker, Kubernetes, Helm	Containerization and orchestration
Observability	Prometheus, Grafana, Jaeger	Metrics, Logs, and Traces

Export to Sheets

🧪 Developer Setup
Prerequisites
Python 3.10+

Node.js 18+

Docker & Docker Compose

1. Clone Repository
Bash

git clone https://github.com/rathishbarath/multi-agent-platform.git
cd multi-agent-platform
2. Backend Setup
Bash

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
3. Worker Setup (Local)
To run a worker locally for debugging:

Bash

celery -A app.worker worker --loglevel=info --pool=solo
4. Frontend Setup
Bash

cd frontend
npm install
npm run dev
🐳 Docker (Full Stack)
For a production-mirror environment, use the composed stack.

Bash

# Build and start all services (API, Workers, Redis, DB, Frontend)
docker-compose up --build -d
Access Points:

API Swagger: http://localhost:8000/docs

Frontend: http://localhost:3000

Flower (Task Monitor): http://localhost:5555

🔐 Environment Variables
Create a backend/.env file. Do not commit this file.

Ini, TOML

# --- Core ---
ENV=development
SECRET_KEY=super_secret_key_change_in_prod

# --- AI Providers ---
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

# --- Vector Database ---
VECTOR_DB_URL=http://localhost:6333
VECTOR_DB_API_KEY=...

# --- Infrastructure ---
REDIS_URL=redis://redis:6379/0
POSTGRES_URL=postgresql://user:pass@db:5432/genai_platform
📘 API Documentation
Start Research Pipeline
POST /api/v1/research/start

JSON

{
  "topic": "The Future of Quantum Computing in Finance",
  "depth": "deep",
  "output_format": ["pdf", "video"]
}
Check Task Status
GET /api/v1/tasks/{task_id}

JSON

{
  "task_id": "c92f-...",
  "status": "PROCESSING",
  "progress": 75,
  "current_stage": "Generating Video Assets"
}
☸️ Docker & Kubernetes
The k8s/ directory contains Helm charts for deployment.

Build Images: docker build -t my-registry/genai-backend:latest .

Deploy:

Bash

helm upgrade --install genai-platform ./k8s/charts
Autoscaling: HPA is configured to scale workers based on Redis queue depth.

🚦 CI/CD
GitHub Actions pipelines are defined in .github/workflows:

ci.yml: Runs pytest, flake8, and mypy on every PR.

cd.yml: Builds Docker images and pushes to ECR/GCR on merge to main.

Required Secrets: DOCKER_USERNAME, DOCKER_PASSWORD, KUBE_CONFIG.

📊 Observability
We use the OpenTelemetry standard for full visibility.

Metrics: Prometheus scrapes /metrics endpoints.

Dashboards: Grafana templates located in ops/grafana/dashboards.

Tracing: Jaeger/Tempo captures request lifecycles from API Gateway → Celery Worker → LLM.

🤝 Contributing
We welcome contributions! Please follow the standard engineering guidelines:

Fork & Clone the repo.

Create a Feature Branch (git checkout -b feature/amazing-feature).

Commit using Conventional Commits (e.g., feat: add mistral support).

Push & PR: Open a Pull Request for review.

📄 License
Distributed under the Apache 2.0 License. See LICENSE for details.

📬 Contact
Rathish Barath

GitHub: @rathishbarath

Email: your_email@example.com

