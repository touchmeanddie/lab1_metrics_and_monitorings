import uuid
import time
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger()


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id,
                                               service="api")

        logger.info(
            "request_started",
            method=request.method,
            route=request.url.path,
        )

        start = time.monotonic()

        try:
            response = await call_next(request)
        except Exception:
            logger.exception("request_failed",
                             route=request.url.path, method=request.method)
            raise

        duration_ms = (time.monotonic() - start) * 1000
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_finished",
            method=request.method,
            route=request.url.path,
            status=response.status_code,
            duration_ms=round(duration_ms, 2)
        )
        return response
