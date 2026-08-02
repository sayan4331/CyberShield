"""Centralized logging setup. Import get_logger(__name__) wherever a module needs to log."""
import logging
import sys

from app.core.config import settings

_CONFIGURED = False


def _configure_root() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s", datefmt="%H:%M:%S"
    ))
    root = logging.getLogger("cybershield")
    root.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    root.addHandler(handler)
    root.propagate = False
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    _configure_root()
    return logging.getLogger(f"cybershield.{name}")
