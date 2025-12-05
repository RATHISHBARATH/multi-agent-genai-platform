import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
sentry_dsn = os.getenv('SENTRY_DSN', '')
if sentry_dsn:
    sentry_sdk.init(dsn=sentry_dsn, integrations=[CeleryIntegration()], traces_sample_rate=0.1)

from celery import Celery
from api.utils.constants import BROKER_URL
# OpenTelemetry for Celery
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import os

resource = Resource.create(attributes={ "service.name": "autoscillab-worker" })
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces"))
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

celery_app = Celery("autoscillab_workers", broker=BROKER_URL, backend=BROKER_URL)
celery_app.conf.task_routes = {
    "api.workers.tasks.*": {"queue": "autoscillab_default"}
}
celery_app.autodiscover_tasks(["api.workers.tasks"])

# instrument celery
CeleryInstrumentor().instrument()
