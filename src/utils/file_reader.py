"""Utility for reading files with caching."""
from pathlib import Path

from src.core.cache import cache


@cache()
def read_text(path: str) -> str:
    """Read a text file from disk and cache the result."""
    return Path(path).read_text(encoding="utf-8")
