import logging
import sys

import structlog

from synapsecord_core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()

    logging.basicConfig(
        format="(%(asctime)s) [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.synapsecord_log_level.upper(), logging.INFO)
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.synapsecord_log_level.upper(), logging.INFO)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True
    )

def get_logger(name: str) -> structlog.BoundLogger:
    return structlog.get_logger(name)
