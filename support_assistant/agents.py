"""Utility functions for interacting with Make scenarios.

This module caches heavy external API calls and provides utilities
for executing scenarios concurrently.
"""

import asyncio
from functools import lru_cache
from typing import Iterable, List

import config

MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


@lru_cache(maxsize=128)
def _connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Simulate triggering a Make scenario.

    The real implementation should handle errors and perform an HTTP call.
    """
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    # Example network call (disabled in this environment):
    # response = requests.post(f"{MAKE_API_BASE}/scenarios/{scenario_id}/run", headers=headers)
    # return response.json()
    return {"status": "connected", "scenario": scenario_id}


def connect_to_make(api_token: str, scenario_id: str) -> dict:
    """Trigger a Make scenario, using cache if enabled."""
    if config.ENABLE_CACHE:
        return _connect_to_make(api_token, scenario_id)
    # Bypass cache by calling the wrapped function directly
    _connect_to_make.cache_clear()
    return _connect_to_make.__wrapped__(api_token, scenario_id)


async def run_scenarios(api_token: str, scenario_ids: Iterable[str]) -> List[dict]:
    """Run multiple scenarios concurrently.

    Each scenario is executed in a thread to avoid blocking the event loop.
    """
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, connect_to_make, api_token, sid) for sid in scenario_ids]
    return await asyncio.gather(*tasks)
