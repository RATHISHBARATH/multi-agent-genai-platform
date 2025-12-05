# Multi-Agent GenAI Platform

[![CI](https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/ci.yaml/badge.svg)](https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/ci.yaml)
[![E2E Celery](https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/e2e-celery.yml/badge.svg)](https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/e2e-celery.yml)
[![CD Pipeline](https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/cd.yaml/badge.svg)](https://github.com/rathishbarath/multi-agent-genai-platform/actions/workflows/cd.yaml)
![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-blue)
![License](https://img.shields.io/badge/License-Apache--2.0-green.svg)

> A production-grade **multi-agent GenAI orchestration platform** that autonomously retrieves research, performs LLM-driven reasoning, generates structured insights, produces narrated videos and PPTs, and indexes knowledge using vector search — built with distributed microservices, Celery pipelines, FastAPI, Next.js, Redis, Postgres, Prometheus, Grafana, OpenTelemetry, and Kubernetes + Helm.

---

# 📌 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Developer Quickstart](#developer-quickstart)
- [Environment Variables](#environment-variables)
- [Workers & Tasks](#workers--tasks)
- [Database & Migrations](#database--migrations)
- [CI/CD Pipelines](#cicd-pipelines)
- [Observability](#observability)
- [Security](#security)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

# 🔥 Overview

This repository demonstrates how enterprise GenAI orchestration systems are built inside companies like:

**Google, Meta, Amazon, Microsoft, Intuit, NVIDIA, OpenAI.**

The platform includes:

- Multi-agent reasoning workflows  
- Research retrieval + LLM summarization  
- Vector embeddings and semantic search  
- Automatic PPT and narrated video generation  
- Distributed Celery pipelines  
- Production-ready monitoring and logging  
- Full CI/CD with DockerHub + Kubernetes  

Perfect for portfolio, interviews, and senior-level engineering showcases.

---

# 🏗 Architecture

## **System Architecture Diagram**

```mermaid
flowchart LR
    subgraph FE [Frontend]
        A[Next.js UI] -->|REST| B[API Gateway (Next.js Proxy)]
    end

    subgraph API [Backend - FastAPI]
        B --> C[FastAPI Application]
        C --> D[Multi-Agent Orchestrator]
        D --> E[LLM API (OpenAI / Local Model)]
        D --> F[Embeddings Service]
        D --> G[Vector DB (Pinecone / SQLite)]
        C --> H[Celery Broker (Redis / RabbitMQ)]
        H --> I[Workers (PPT, Video, Ingest)]
        C --> J[Postgres (SQLModel)]
        C --> K[Redis Cache]
        C --> L[Prometheus Metrics + OTel Tracing]
    end

    subgraph Infra [Cloud / Kubernetes]
        G --> M[Pinecone Cloud]
        L --> N[Grafana Dashboard]
        L --> O[OpenTelemetry Collector]
    end
🌟 Features
🧠 Multi-Agent Orchestration
SearchAgent → retrieve research

SummarizerAgent → LLM summarization

IngestAgent → embeddings + indexing

MediaAgent → PPT & narrated video generation

⚡ Distributed Execution
Async FastAPI

Celery workers

Redis/RabbitMQ broker

Real-time task tracking

🎥 Automated Media Generation
PPT (python-pptx)

Narrated video (MoviePy + gTTS + ffmpeg)

🔍 Semantic Search
Pinecone

SentenceTransformers

SQLite fallback

📈 Observability
OpenTelemetry

Prometheus + Grafana

JSON logging

Task monitoring panels

🛡 Security
JWT auth

Rate limiting

Sentry error tracking

NetworkPolicies

PodSecurity

⚙️ Tech Stack
Backend
FastAPI, SQLModel, Celery, Redis, Postgres, httpx

Frontend
Next.js 13, React, Tailwind

Embeddings & Vector Search
SentenceTransformers, Pinecone, SQLite Fallback

Media
MoviePy, gTTS, python-pptx

DevOps
Docker, Kubernetes, Helm, GitHub Actions

🧪 Developer Quickstart
Clone repository
bash
Copy code
git clone https://github.com/rathishbarath/multi-agent-genai-platform
cd multi-agent-genai-platform
Start backend stack
bash
Copy code
cd infra
docker-compose up --build
Start frontend
bash
Copy code
cd frontend/nextjs-app
npm install
npm run dev
🔐 Environment Variables
Create .env in backend/api:

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
🏭 Workers & Tasks
Start Celery worker:

bash
Copy code
cd backend/workers
celery -A api.workers.celery_app.celery_app worker --loglevel=info
Tasks:

orchestrate_research

summarization

vector_ingest

generate_ppt

generate_video

🗄 Database & Migrations
Run migrations:

bash
Copy code
cd backend/api
alembic upgrade head
🧪 CI/CD Pipelines
✔ ci.yaml
Build + Lint + Tests

✔ e2e-celery.yml
Starts Redis + Postgres + Worker, runs full pipeline test

✔ cd.yaml
Builds Docker image
Pushes to DockerHub
Deploys to Kubernetes

Secrets required:

nginx
Copy code
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
KUBE_CONFIG_DATA
📊 Observability
Metrics
Prometheus endpoint: /metrics

Dashboards
Import these from /grafana:

dashboard_full.json

dashboard_enterprise.json

Tracing
OpenTelemetry exporters enabled.

Logs
Structured JSON logs via python-json-logger.

🔒 Security
JWT

Rate limiting

Sentry

PodSecurity restrict

NetworkPolicies

RBAC for secrets

🚀 Deployment
Docker
bash
Copy code
docker-compose up --build
Kubernetes
bash
Copy code
kubectl apply -f infra/kubernetes/
Helm
bash
Copy code
helm install autoscillab helm/
🤝 Contributing
Follow Conventional Commits:

vbnet
Copy code
feat: add summarizer agent
fix: redis reconnect logic
docs: update architecture diagram
refactor: orchestrator async improvements
📄 License
Apache 2.0

📬 Contact
Maintainer: Rathish Barath
GitHub: https://github.com/rathishbarath
Email: YOUR_EMAIL
