"""Retry utilities for network and file operations.

Provides a simple exponential backoff implementation without external
dependencies.
"""
from __future__ import annotations

import json
import time
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable[..., object])


def retry_on_exception(*, max_attempts: int = 3, base: int = 2) -> Callable[[F], F]:
    """Decorator providing retry with exponential backoff.

    Args:
        max_attempts: Maximum number of retries before giving up.
        base: Initial delay and multiplier for backoff.

    Returns:
        Decorator applying retry logic to the wrapped function.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    time.sleep(delay)
                    delay *= base

        return wrapper  # type: ignore[return-value]

    return decorator


@retry_on_exception()
def load_json(path: str | Path) -> object:
    """Load a JSON file with retry support."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
