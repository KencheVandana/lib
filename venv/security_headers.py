from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from custom_logging import setup_logging

logger = setup_logging()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Apply security headers, excluding Swagger UI endpoints
        if not (request.url.path.startswith("/docs") or request.url.path.startswith("/redoc")):
            response.headers["Content-Security-Policy"] = "default-src 'self';"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Referrer-Policy"] = "no-referrer"

            logger.info(f"Applied security headers to {request.url.path}")

        return response
