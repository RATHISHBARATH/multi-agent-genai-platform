import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import research, agents, video, ppt, ingest, health
from .auth import oauth2_scheme
from .utils.metrics import metrics_response
from api.middleware import register
from starlette_helmet import HelmetMiddleware
import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
sentry_dsn = os.getenv('SENTRY_DSN', '')
if sentry_dsn:
    sentry_logging = LoggingIntegration(level=None, event_level=None)
    sentry_sdk.init(dsn=sentry_dsn, integrations=[sentry_logging, CeleryIntegration()], traces_sample_rate=0.1)


# OpenTelemetry initialization
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource.create(attributes={
    "service.name": "autoscillab-api",
    "service.version": "0.2.0"
})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces"))
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI(title="AutoSciLab Ultra API", version="0.2.0")
# security headers
app.add_middleware(HelmetMiddleware)
# rate limiter
register(app)
# Sentry middleware (wrap ASGI app)
if sentry_dsn:
    app.add_middleware(SentryAsgiMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# instrument the app to create telemetry
FastAPIInstrumentor.instrument_app(app)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(research.router, prefix="/research", tags=["research"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(video.router, prefix="/video", tags=["video"])
app.include_router(ppt.router, prefix="/ppt", tags=["ppt"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])

app.add_api_route('/metrics', metrics_response, methods=['GET'])

@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    # returns service status and token subject if provided
    return {"service": "AutoSciLab Ultra API", "status": "ok"}
