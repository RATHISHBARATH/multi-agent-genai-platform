"""Rate limiting middleware using slowapi (redis backend recommended)."""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request
from fastapi.responses import JSONResponse

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.errors import RateLimitExceeded

# Limiter - default in-memory; for production use Redis storage
limiter = Limiter(key_func=get_remote_address)

def register(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
