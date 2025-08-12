import logging
from typing import Optional

_LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT)


def get_logger(run_id: Optional[str] = None, step_id: Optional[str] = None) -> logging.Logger:
    """Return a logger with contextual information."""
    logger = logging.getLogger(f"agentic.{run_id}.{step_id}")
    return logger
