"""Centralized logging configuration for the assistant project."""

import logging
import sys
from typing import Optional, TextIO


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    stream: Optional[TextIO] = None,
) -> None:
    """
    Configure logging for the entire application.

    Args:
        level: Logging level (default: logging.INFO)
        format_string: Custom format string. If None, uses default format.
        stream: Output stream. If None, uses sys.stderr.
    """
    if format_string is None:
        format_string = "%(asctime)s %(levelname)s %(name)s: %(message)s"

    if stream is None:
        stream = sys.stderr

    logging.basicConfig(
        level=level,
        format=format_string,
        stream=stream,
        force=True,  # Override any existing configuration
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.

    Args:
        name: Logger name (typically __name__ of the calling module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
