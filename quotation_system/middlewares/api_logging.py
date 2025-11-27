import time
import uuid

import structlog

logger = structlog.get_logger()


class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer
        start_time = time.monotonic()

        # Add request ID and context
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.path,
            method=request.method,
            user_id=getattr(request.user, "id", None),
            ip=request.META.get("REMOTE_ADDR"),
        )

        response = self.get_response(request)

        # Calculate response time
        duration = time.monotonic() - start_time  # seconds (float)
        duration_ms = round(duration * 1000, 2)  # ms

        # Log the completed request
        logger.info(
            "request_finished",
            status=response.status_code,
            duration_ms=duration_ms,
        )

        # Clear context for next request
        structlog.contextvars.clear_contextvars()

        return response
