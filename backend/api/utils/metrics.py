from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

REQUEST_COUNT = Counter('autoscillab_request_count', 'Number of requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('autoscillab_request_latency_seconds', 'Request latency seconds', ['endpoint'])

def metrics_response():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
