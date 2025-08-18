"""Retry decorator with exponential backoff."""
from __future__ import annotations

import time
from functools import wraps
from typing import Callable, Tuple, Type, TypeVar

from ..config import retry_config

F = TypeVar("F", bound=Callable[..., object])


def retry(
    *,
    exceptions: Tuple[Type[BaseException], ...] | Type[BaseException] | None = None,
    max_attempts: int | None = None,
    backoff_factor: float | None = None,
) -> Callable[[F], F]:
    """Retry decorator with exponential backoff.

    Parameters default to the values defined in :mod:`nexus.config`.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore[misc]
            cfg = retry_config
            if not cfg.enabled:
                return func(*args, **kwargs)

            excs = exceptions or cfg.exceptions
            if not isinstance(excs, tuple):
                excs = (excs,)

            attempts = max_attempts or cfg.max_attempts
            delay = backoff_factor or cfg.backoff_factor

            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except excs:
                    if attempt >= attempts:
                        raise
                    time.sleep(delay)
                    delay *= 2

        return wrapper  # type: ignore[return-value]

    return decorator
