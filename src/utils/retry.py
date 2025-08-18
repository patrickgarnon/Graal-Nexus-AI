import logging
import random
import time
from functools import wraps
from typing import Callable, Iterable, Optional, Type


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    jitter: float = 0.5,
    exceptions: Iterable[Type[Exception]] = (Exception,),
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """Retry calling the decorated function using exponential backoff with jitter.

    Args:
        max_attempts: Total number of attempts before giving up.
        base_delay: Initial delay between retries in seconds.
        jitter: Maximum random jitter added to the delay.
        exceptions: Exceptions that trigger a retry.
        logger: Optional logger instance; defaults to module logger.
    """

    log = logger or logging.getLogger(__name__)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    log.info("Attempt %d for %s", attempt, func.__name__)
                    return func(*args, **kwargs)
                except tuple(exceptions) as exc:
                    if attempt >= max_attempts:
                        log.error("Giving up after %d attempts due to: %s", attempt, exc)
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    delay += random.uniform(0, jitter)
                    log.warning(
                        "Attempt %d failed with %s. Retrying in %.2f seconds", attempt, exc, delay
                    )
                    time.sleep(delay)
                    attempt += 1

        return wrapper

    return decorator
