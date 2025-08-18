"""Central logging utilities for the Nexus project.

Provides a JSON-formatted logger with configurable levels via
environment variable or command-line option.
"""

from __future__ import annotations

import logging
import os
import json
from typing import Optional


class JsonFormatter(logging.Formatter):
    """Format log records as JSON for cloud-friendly logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """Configure root logger.

    The log level can be provided directly, through the ``level`` argument,
    via the ``LOG_LEVEL`` environment variable, or defaults to ``INFO``.
    """

    level_name = level or os.getenv("LOG_LEVEL", "INFO")
    level_name = level_name.upper()
    logging.basicConfig(level=getattr(logging, level_name, logging.INFO))
    formatter = JsonFormatter()
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(formatter)
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the given name."""
    return logging.getLogger(name)

