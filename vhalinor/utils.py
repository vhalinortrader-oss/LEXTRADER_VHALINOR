"""Utilitários compartilhados (logging, tempo, helpers numéricos)."""
from __future__ import annotations

import logging
import os
import sys
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from loguru import logger

from .config import logs_dir


_configured = False


def setup_logger(level: str = "INFO") -> None:
    """Configura o loguru uma única vez, escrevendo em stdout e em `logs/lextrader.log`."""
    global _configured
    if _configured:
        return
    _configured = True

    logger.remove()
    logger.add(sys.stderr, level=level, enqueue=False, backtrace=False, diagnose=False,
               format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> | "
                      "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

    log_path: Path = logs_dir() / "lextrader.log"
    logger.add(str(log_path), level=level, rotation="5 MB", retention=3, enqueue=True,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level: <7} | {name}:{function} - {message}")


def timeit(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        dt = (time.perf_counter() - t0) * 1000
        logger.debug(f"{fn.__name__} executou em {dt:.1f} ms")
        return result
    return wrapper


def utcnow() -> datetime:
    return datetime.utcnow()


def safe_pct_change(old: float, new: float) -> float:
    if old == 0:
        return 0.0
    return (new - old) / old
