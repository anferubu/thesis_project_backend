"""
This module provides logging functionality for FastAPI applications. It includes a middleware class `LogRequestsMiddleware` for logging HTTP requests
and responses.
"""

from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware



formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

handler = TimedRotatingFileHandler(
    "logs/log",
    when="m",
    interval=5,
    backupCount=6,
    encoding="utf-8"
)

handler.setFormatter(formatter)

logger = logging.getLogger("api_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)



class LogRequestsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    """

    async def dispatch(self, request:Request, call_next):
        start_time = datetime.now()

        response = await call_next(request)

        end_time = datetime.now()
        duration = end_time - start_time

        log_data = {
            "method": request.method,
            "url": str(request.url),
            "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": duration.total_seconds(),
            "ip": request.client.host,
            "status_code": response.status_code,
            "user_agent": request.headers.get("user-agent", "-"),
            "referer": request.headers.get("referer", "-"),
            "cookies": request.cookies,
            "query_params": dict(request.query_params),
        }

        status_code = response.status_code

        if status_code >= 500:
            log_level = logging.ERROR
        elif status_code >= 400:
            log_level = logging.WARNING
        else:
            log_level = logging.INFO

        logger.log(log_level, log_data)

        return response