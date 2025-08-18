# File: logging_config.py

import logging
import json
import os
import uuid
from datetime import datetime, timezone
from flask import g, request


class JsonLogFormatter(logging.Formatter):
    # type: ignore[override]
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        # Inject correlation/request info if present on record (added in middleware)
        for attr in ("correlation_id", "path", "method", "latency_ms"):
            if hasattr(record, attr):
                payload[attr] = getattr(record, attr)
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(app):
    desired_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
    app.logger.setLevel(getattr(logging, desired_level, logging.DEBUG))

    # Prevent duplicate handlers (e.g., on reload / tests)
    if any(isinstance(h, logging.FileHandler) for h in app.logger.handlers):
        return

    os.makedirs('./logs', exist_ok=True)
    file_handler = logging.FileHandler('./logs/app.log')
    file_handler.setLevel(getattr(logging, desired_level, logging.DEBUG))

    structured = os.getenv("LOG_FORMAT", "text").lower() == "json"
    if structured:
        formatter = JsonLogFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Middleware-like hooks for correlation ID and timing
    @app.before_request
    def _assign_correlation_id():  # pragma: no cover (thin wrapper)
        g.start_ts = datetime.now(tz=timezone.utc)
        g.correlation_id = request.headers.get(
            'X-Request-ID', str(uuid.uuid4()))

    @app.after_request
    def _log_request(response):  # pragma: no cover
        try:
            latency = None
            if hasattr(g, 'start_ts'):
                latency = (datetime.now(tz=timezone.utc) -
                           g.start_ts).total_seconds() * 1000
            extra = {
                'correlation_id': getattr(g, 'correlation_id', None),
                'path': request.path,
                'method': request.method,
            }
            if latency is not None:
                extra['latency_ms'] = round(latency, 2)
            app.logger.info(
                f"{request.method} {request.path} {response.status_code}", extra=extra)
            # Echo correlation id back
            if getattr(g, 'correlation_id', None):
                response.headers['X-Request-ID'] = g.correlation_id
        except Exception:
            app.logger.debug("Request logging hook failed", exc_info=True)
        return response
