[![Integration Matrix](https://github.com/yourorg/autoscillab-ultra/actions/workflows/integration-matrix.yml/badge.svg)](https://github.com/yourorg/autoscillab-ultra/actions/workflows/integration-matrix.yml)
[![E2E Celery](https://github.com/yourorg/autoscillab-ultra/actions/workflows/e2e-celery.yml/badge.svg)](https://github.com/yourorg/autoscillab-ultra/actions/workflows/e2e-celery.yml)

# AutoSciLab Ultra — Complete (Observability + CI/CD + Tests)

[![CI](https://github.com/yourorg/autoscillab-ultra/actions/workflows/ci.yaml/badge.svg)](https://github.com/yourorg/autoscillab-ultra/actions)
[![CD](https://github.com/yourorg/autoscillab-ultra/actions/workflows/cd.yaml/badge.svg)](https://github.com/yourorg/autoscillab-ultra/actions)

## Architecture (Mermaid)

```mermaid
flowchart LR
  A[User • Frontend (Next.js)] -->|REST| B[API • FastAPI]
  B --> C[Orchestrator]
  C --> D[LLM API]
  C --> E[Embeddings (sentence-transformers)]
  C --> F[Pinecone / VectorDB]
  C --> G[Kafka (events)]
  B --> H[Celery Workers]
  H --> I[VideoGen / PPT Creator]
  B --> J[Postgres / Redis / Metrics]
  subgraph Observability
    K[Prometheus] --> L[Grafana]
    M[OpenTelemetry Collector] --> K
  end
```
## Developer Onboarding (local)

1. Clone repo
2. Copy env examples / set env vars (see `.env.example`):
```
JWT_SECRET=change_me
LLM_API_KEY=sk-...
PINECONE_API_KEY=pc-...
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
```
3. Start infra (redis + api + worker):
```
cd infra
docker-compose up --build
# optionally: docker-compose -f docker-compose.kafka.yaml up --build
```
4. Start frontend:
```
cd frontend/nextjs-app
npm install
npm run dev
```
5. Run tests:
```
# in backend dir
pytest backend/tests/integration/test_e2e.py
```
6. CI/CD: Configure GitHub repo secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `KUBE_CONFIG_DATA`.

## Observability & Monitoring
- Metrics: `/metrics` endpoint (Prometheus)
- Traces: OTLP exporter to OpenTelemetry Collector or hosted solution
- Dashboards: `grafana/dashboard_full.json` for import

## Notes
- The repo provides safe fallbacks: local SQLite vector DB and in-memory Kafka for dev when external services or keys are missing.
- Replace secrets and API keys before deploying to public clouds.


# AutoSciLab Ultra (Showcase)

This repository is a production-style showcase for an enterprise GenAI research orchestration platform.
It includes:
- FastAPI backend + modular routers and services
- Celery worker stubs (Redis broker)
- Next.js frontend with a proxy API
- Dockerfiles and docker-compose for local demo
- Kubernetes manifests (placeholders) for cloud deployment
- Prometheus / Grafana placeholders

**Usage (local demo)**

1. Start redis and services with Docker Compose (from infra directory):
   ```
   cd infra
   docker-compose up --build
   ```
2. Start frontend:
   ```
   cd frontend/nextjs-app
   npm install
   npm run dev
   ```
3. API: http://localhost:8000
   Frontend: http://localhost:3000

Replace placeholder implementations with real LLM integrations, vector DBs (Pinecone/Weaviate), Kafka, and production-grade auth (OAuth2/JWT).


## Added features: Pinecone, Kafka, Helm, CD pipeline

### Quickstart (local)
- Set environment variables (example):
```
export JWT_SECRET="change_me"
export LLM_API_KEY="sk-..."
export PINECONE_API_KEY="pc-..."
```
- Start Redis + API + Worker: from infra directory run `docker-compose up --build`
- To run Kafka locally: `docker-compose -f infra/docker-compose.kafka.yaml up --build`
- Use sqlite-based vector DB by default if Pinecone is not configured.

### CI/CD
- CD workflow builds Docker images and pushes to Docker Hub. Set `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in repo secrets.
- Deployment step expects `KUBE_CONFIG_DATA` secret with base64 kubeconfig to apply manifests in `infra/kubernetes`.



## Database / Models / Migrations

This project uses `SQLModel` for models (see `backend/api/models/models.py`). For production, use Postgres.

Migrations with Alembic:
1. Install requirements: `pip install -r backend/api/requirements.txt`
2. Initialize alembic in `backend/api` with `alembic init migrations`
3. Configure alembic.ini to point to your DATABASE_URL (Postgres)
4. Use `sqlmodel`'s metadata for autogenerate
5. Example migration commands:
   - `alembic revision --autogenerate -m "init"`
   - `alembic upgrade head`


## Postgres & Migrations

This repo uses Postgres in docker-compose. To initialize DB:

```
cd infra
docker-compose up -d postgres
# in backend/api
pip install -r requirements.txt
alembic init alembic  # if not done
# configure alembic.ini sqlalchemy.url to point to DATABASE_URL_SYNC or set env var
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Celery Workers & Tasks

Start worker (requires redis/broker running):

```
cd backend/workers
# run celery worker process, ensure PYTHONPATH includes backend/api
celery -A api.workers.celery_app.celery_app worker --loglevel=info
```

API endpoints:
- `/agents/start_research` POST {q: "..."} -> returns task_id
- `/agents/task_status/{task_id}` GET -> returns task DB row



## Ultimate Mode Additions (Async + Rate Limiting + Security)

- Core services (paper retriever, scraper, agents, orchestrator) are async and use `httpx` for non-blocking I/O.
- Celery tasks call async orchestrator via `asyncio.run(...)` to bridge sync workers and async code.
- Rate limiting implemented via `slowapi`. For production, configure Redis storage for `Limiter`.
- Security headers are applied with `starlette-helmet` middleware.
- Tests added: `backend/tests/integration/test_orchestrator_async.py` (pytest-asyncio)



## Enterprise Additions: E2E Tests, Security, Logging, Sentry

### E2E Celery Tests
- Workflow: `.github/workflows/e2e-celery.yml` will run the Celery e2e test using services (Postgres/Redis/RabbitMQ).
- The test `backend/tests/integration/test_celery_e2e.py` starts a research task and polls `/agents/task_status/{task_id}` until completion to assert success.

### Security & Kubernetes
- NetworkPolicies: `infra/kubernetes/networkpolicy.yaml` denies by default and allows app-specific traffic.
- Pod Security: `infra/kubernetes/podsecurity.yaml` enforces `restricted` profile for the `autoscillab` namespace.
- Secrets rotation: use `external-secrets` with secret stores or sealed-secrets for git-safe secrets. Example: `infra/kubernetes/external_secret_rotation.yaml`
- RBAC role to allow secrets access: `infra/kubernetes/rbac-secrets.yaml`

### Logging & Error Reporting
- Structured JSON logs are enabled via `python-json-logger` in `api/utils/logging.py`.
- Sentry integration: set `SENTRY_DSN` env var to enable error reporting and tracing for both API and Celery workers.
- Grafana dashboard includes panels for task success rates and task events; import `grafana/dashboard_enterprise.json`.


## Architecture

```mermaid
flowchart LR
  subgraph FE [Frontend]
    A[Next.js UI] -->|REST| B[API Gateway / Next.js API]
  end
  subgraph API [Backend]
    B --> C[FastAPI App]
    C --> D[Orchestrator (Agents)]
    D --> E[LLM API]
    D --> F[Embeddings Service]
    D --> G[Vector DB (Pinecone/SQLite)]
    C --> H[Celery (Broker: Redis/RabbitMQ)]
    H --> I[Workers (Video/PPT/Indexing)]
    C --> J[Postgres (SQLModel)]
    C --> K[Redis (cache)]
    C --> L[Prometheus + OpenTelemetry]
  end
  subgraph Infra[Cluster]
    G --> M[Pinecone (managed)]
    L --> N[Grafana]
    L --> O[Sentry / OTLP Collector]
  end
```
