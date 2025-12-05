
FROM python:3.11-slim
WORKDIR /app
COPY ../api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ../api /app/api
COPY . /app/workers
ENV PYTHONUNBUFFERED=1
CMD ["celery", "-A", "api.workers.celery_app.celery_app", "worker", "--loglevel=info"]
