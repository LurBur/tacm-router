"""Logging configuration for Siphon MVP service."""

import logging
import sys
from typing import Optional
from app.config import settings


def get_logger(name: str) -> logging.Logger:
    """Get configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    return logger


class RequestContextFilter(logging.Filter):
    """Filter to add request ID to log records."""
    
    def __init__(self):
        super().__init__()
        self.default_request_id = "no-request-id"
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add request_id to log record."""
        if not hasattr(record, "request_id"):
            record.request_id = self.default_request_id
        return True


def configure_logging():
    """Configure root logger and add request context filter."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Add request context filter to all handlers
    for handler in root_logger.handlers:
        handler.addFilter(RequestContextFilter())
