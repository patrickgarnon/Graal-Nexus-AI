"""Integration helpers for the Make API."""
import requests
from typing import Dict

MAKE_API_BASE = "https://api.make.com/v2"


def get_scenario_stats(api_token: str, scenario_id: str) -> Dict[str, float]:
    """Return key metrics for a Make scenario.

    Parameters
    ----------
    api_token: str
        Personal access token for the Make API.
    scenario_id: str
        Identifier of the scenario to inspect.

    Returns
    -------
    dict
        Dictionary containing metrics such as total operations, success rate
        and average execution time. On error, an ``error`` key is added with
        a message and the metrics default to ``0``.
    """
    headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
    url = f"{MAKE_API_BASE}/scenarios/{scenario_id}/statistics"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "total_operations": data.get("operationsCount", 0),
            "success_rate": data.get("successRate", 0),
            "avg_exec_time": data.get("executionTimeAvg", 0),
        }
    except Exception as exc:  # pragma: no cover - network failures not tested
        return {
            "error": str(exc),
            "total_operations": 0,
            "success_rate": 0,
            "avg_exec_time": 0,
        }
