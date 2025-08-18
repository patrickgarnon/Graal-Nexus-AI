"""Simple caching utilities for API responses.

Uses `diskcache` for persistent caching with optional TTL expiration. If
`diskcache` is not available, falls back to an in-memory LRU cache.

Functions decorated with ``@cached`` gain an ``invalidate`` attribute to clear
cached values manually.
"""
from __future__ import annotations

import os
from functools import lru_cache, wraps
from typing import Any, Callable, Optional

try:  # Prefer persistent disk cache when available
    from diskcache import Cache as DiskCache

    _CACHE_DIR = os.environ.get("CACHE_DIR", ".cache")
    _disk_cache = DiskCache(_CACHE_DIR)

    def cached(ttl: Optional[int] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Cache decorator with optional TTL using ``diskcache``.

        Args:
            ttl: Time-to-live in seconds for cached values. ``None`` means no
                expiration.
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            memoized = _disk_cache.memoize(expire=ttl)(func)

            def invalidate(*args: Any, **kwargs: Any) -> None:
                """Invalidate cached value for specific call or entire cache."""
                if args or kwargs:
                    key = _disk_cache.memoize_key(func, *args, **kwargs)
                    _disk_cache.delete(key)
                else:
                    _disk_cache.clear()

            memoized.invalidate = invalidate  # type: ignore[attr-defined]
            return memoized

        return decorator

    def clear_cache() -> None:
        """Clear the entire disk cache."""
        _disk_cache.clear()

except ImportError:  # Fall back to in-memory LRU cache
    def cached(ttl: Optional[int] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Simple LRU cache decorator.

        ``ttl`` is ignored in this fallback implementation.
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            cached_func = lru_cache(maxsize=None)(func)

            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return cached_func(*args, **kwargs)

            def invalidate() -> None:
                cached_func.cache_clear()

            wrapper.invalidate = invalidate  # type: ignore[attr-defined]
            return wrapper

        return decorator

    def clear_cache() -> None:
        """No-op clear when using LRU cache."""
        pass

__all__ = ["cached", "clear_cache"]
