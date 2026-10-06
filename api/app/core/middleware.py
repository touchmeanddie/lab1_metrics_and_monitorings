import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.metrics import (
    http_requests_total,
    http_request_duration_seconds,
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        route = request.scope.get("route")
        route_template = route.path if route else request.url.path

        http_requests_total.labels(
            method=request.method,
            route=route_template,
            status=str(response.status_code),
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            route=route_template,
        ).observe(duration)

        return response
