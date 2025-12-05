# Troubleshooting Guide — AutoSciLab Ultra

This guide lists common issues when running the integration tests locally or in CI, and gives fixes.

## 1) Docker containers not healthy (Postgres/Redis/RabbitMQ)
Symptoms:
- CI job times out waiting for services.
Fixes:
- Ensure Docker has sufficient memory (>= 4GB) and CPU.
- Increase health check retries or sleep delays in CI/workflow scripts.
- Inspect logs: `docker-compose -f infra/docker-compose.yaml logs postgres`.

## 2) Celery tasks never complete
Symptoms:
- API returns task_id but `/agents/task_status/{id}` remains `pending` or `running`.
Fixes:
- Ensure Celery worker is running and connected to the same broker (Redis/RabbitMQ).
- Start worker manually: `celery -A api.workers.celery_app.celery_app worker --loglevel=info`.
- Check worker logs for exceptions. Sentry will capture stack traces if `SENTRY_DSN` is set.

## 3) Database connection errors
Symptoms:
- Asyncpg connection errors or missing DB.
Fixes:
- Check `DATABASE_URL_ASYNC` and `DATABASE_URL_SYNC` env vars.
- If using Docker, confirm the `postgres` service is listening on `5432` and healthy.
- For CI use sqlite: the integration matrix supports `sqlite` variant to speed tests.

## 4) LLM/Embedding model failures or memory OOM
Symptoms:
- `transformers` out of memory or slow initial load.
Fixes:
- Use OpenAI via `LLM_API_KEY` instead of local `transformers` for CI.
- For local testing, reduce model size (`all-MiniLM-L6-v2`) or use fallback hash embedder.

## 5) Sentry not capturing errors
Symptoms:
- Errors not visible in Sentry dashboard even after setting `SENTRY_DSN`.
Fixes:
- Ensure `SENTRY_DSN` is exported before starting services (API & Celery).
- Confirm DSN is valid and organization has ingest enabled for the environment.

## 6) Test flakiness (timeouts)
Symptoms:
- Intermittent test failures, especially under CI load.
Fixes:
- Increase timeouts in `backend/tests/integration/*` (E2E_TIMEOUT env var).
- Add retries for network calls and backoff to external APIs or mock them in CI.

If you hit an issue not covered here, paste error output in the chat and I'll help debug.
