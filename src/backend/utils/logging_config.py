# File: logging_config.py

import logging
import json
import os
from datetime import datetime, timezone


class JsonLogFormatter(logging.Formatter):
    # type: ignore[override]
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
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
