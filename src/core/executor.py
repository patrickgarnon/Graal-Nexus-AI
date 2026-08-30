"""Concurrent execution utilities for Make scenarios.

This module provides an asynchronous executor that can trigger multiple
Make scenarios concurrently. It uses :mod:`asyncio` together with a
:class:`concurrent.futures.ThreadPoolExecutor` so that blocking network
calls performed with ``requests`` can run in parallel.

The public entry point is :func:`run_scenarios` which accepts an API
``token``, an iterable of ``scenario_ids`` and a ``max_workers`` value.
The function schedules the work in a thread pool and gathers the
results once all workers have finished.

Example
-------
>>> import asyncio
>>> from core.executor import run_scenarios
>>> asyncio.run(run_scenarios("token", ["1", "2"]))
[{"status": "connected", "scenario": "1"}, {"status": "connected", "scenario": "2"}]
"""
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List, Dict

import requests

MAKE_API_BASE = "https://api.make.com/v2"  # Placeholder base URL


def _trigger_scenario(api_token: str, scenario_id: str) -> Dict[str, str]:
    """Synchronously trigger a Make scenario.

    Parameters
    ----------
    api_token:
        Authentication token for the Make API.
    scenario_id:
        Identifier of the scenario to trigger.

    Returns
    -------
    dict
        A minimal dictionary describing the result. In a real
        environment this function would issue an HTTP request via
        :func:`requests.post` and return the server response. As the
        execution environment here has no external network access, the
        function returns a simulated response instead.
    """

    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    url = f"{MAKE_API_BASE}/scenarios/{scenario_id}/run"

    try:
        # The actual request is commented out as this environment lacks
        # internet access. Uncomment in a real deployment.
        # response = requests.post(url, headers=headers)
        # response.raise_for_status()
        # return response.json()
        # Simulate network latency so concurrency can be observed when
        # running tests locally.
        import time

        time.sleep(0.1)
        return {"status": "connected", "scenario": scenario_id}
    except requests.RequestException as exc:  # pragma: no cover - network unreachable
        return {"status": "error", "scenario": scenario_id, "detail": str(exc)}


async def run_scenarios(
    api_token: str,
    scenario_ids: Iterable[str],
    max_workers: int = 5,
) -> List[Dict[str, str]]:
    """Trigger several Make scenarios concurrently.

    Parameters
    ----------
    api_token:
        Authentication token for the Make API.
    scenario_ids:
        Iterable of scenario identifiers.
    max_workers:
        Maximum number of worker threads to use for concurrent
        execution.

    Returns
    -------
    list of dict
        A list containing the result for each scenario in the order they
        were provided.
    """

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [
            loop.run_in_executor(executor, _trigger_scenario, api_token, sid)
            for sid in scenario_ids
        ]
        return await asyncio.gather(*tasks)
