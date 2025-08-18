"""Simple HTTP client functions using the configured cache."""
import requests

from src.core.cache import cache


@cache()
def get(url: str, **kwargs):
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response.json()


@cache()
def post(url: str, **kwargs):
    response = requests.post(url, **kwargs)
    response.raise_for_status()
    return response.json()
