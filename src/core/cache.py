"""Caching utilities supporting in-memory LRU and optional Redis backend."""
from __future__ import annotations

import functools
import pickle
from pathlib import Path
from typing import Any, Callable

import yaml

try:  # Optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - redis is optional
    redis = None

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"


def _load_config(path: Path = CONFIG_PATH) -> dict:
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return {}


class CacheManager:
    """Provide a decorator for caching based on configuration."""

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or _load_config()
        cache_conf = self.config.get("cache", {})
        self.backend = cache_conf.get("backend", "memory")
        self.client = None
        if self.backend == "redis":
            if redis is None:
                raise RuntimeError("Redis backend requires the redis package")
            redis_conf = cache_conf.get("redis", {})
            self.client = redis.Redis(
                host=redis_conf.get("host", "localhost"),
                port=redis_conf.get("port", 6379),
                db=redis_conf.get("db", 0),
            )

    def _make_key(self, func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
        return f"{func.__module__}.{func.__name__}:{args}:{sorted(kwargs.items())}"

    def decorator(self, maxsize: int = 128) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        if self.backend == "redis" and self.client is not None:
            def _redis_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
                @functools.wraps(func)
                def wrapper(*args: Any, **kwargs: Any) -> Any:
                    key = self._make_key(func, args, kwargs)
                    cached = self.client.get(key)
                    if cached is not None:
                        return pickle.loads(cached)
                    result = func(*args, **kwargs)
                    self.client.set(key, pickle.dumps(result))
                    return result
                return wrapper
            return _redis_decorator
        else:
            return functools.lru_cache(maxsize=maxsize)


_cache_manager = CacheManager()


def cache(maxsize: int = 128) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Return a decorator implementing the configured cache backend."""
    return _cache_manager.decorator(maxsize=maxsize)
