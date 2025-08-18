"""Utilities for interacting with the Make.com API.

This module provides a small client wrapping the Make REST API endpoints
used by the application. It allows listing scenarios, checking their
executions and statuses and triggering a scenario run on demand.

All functions rely on the ``requests`` library and raise ``RuntimeError``
with a helpful message when a call to the API fails.  In production the
``MakeClient`` can easily be extended with additional endpoints as
needed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests

BASE_URL = "https://api.make.com/v2"


@dataclass
class MakeClient:
    """Simple client for the Make.com API."""

    api_token: str
    base_url: str = BASE_URL

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json",
        }

    # Scenario related -------------------------------------------------
    def list_scenarios(self) -> List[Dict[str, Any]]:
        """Return the list of scenarios available for the account."""
        resp = requests.get(f"{self.base_url}/scenarios", headers=self.headers)
        if resp.ok:
            data = resp.json()
            # API returns objects in ``data``; fall back to raw response.
            return data.get("data", data)
        raise RuntimeError(f"Error listing scenarios: {resp.status_code} {resp.text}")

    def list_scenario_executions(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Return executions for a given scenario."""
        resp = requests.get(
            f"{self.base_url}/scenarios/{scenario_id}/executions",
            headers=self.headers,
        )
        if resp.ok:
            data = resp.json()
            return data.get("data", data)
        raise RuntimeError(
            f"Error listing executions for scenario {scenario_id}: {resp.status_code} {resp.text}"
        )

    # Execution related ------------------------------------------------
    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Return details about a specific execution."""
        resp = requests.get(
            f"{self.base_url}/executions/{execution_id}", headers=self.headers
        )
        if resp.ok:
            return resp.json()
        raise RuntimeError(
            f"Error retrieving execution {execution_id}: {resp.status_code} {resp.text}"
        )

    # Trigger scenario --------------------------------------------------
    def run_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Trigger execution of a scenario and return the API response."""
        resp = requests.post(
            f"{self.base_url}/scenarios/{scenario_id}/run", headers=self.headers
        )
        if resp.ok:
            return resp.json()
        raise RuntimeError(
            f"Error running scenario {scenario_id}: {resp.status_code} {resp.text}"
        )


# Helper functions ------------------------------------------------------
def get_campaign_stats(client: MakeClient) -> Dict[str, Any]:
    """Compute high level metrics for the user's campaigns.

    The function aggregates the number of scenarios, executions and the
    count of executions by status. It is designed to be light‑weight and
    safe to call even when some API calls fail; in that case the partial
    statistics gathered so far are returned.
    """

    stats = {"scenarios": 0, "executions": 0, "statuses": {}}

    try:
        scenarios = client.list_scenarios()
    except Exception:
        return stats

    stats["scenarios"] = len(scenarios)

    for scenario in scenarios:
        scenario_id = str(scenario.get("id") or scenario.get("scenario_id"))
        try:
            executions = client.list_scenario_executions(scenario_id)
        except Exception:
            continue

        stats["executions"] += len(executions)
        for execution in executions:
            status = execution.get("status", "unknown")
            stats["statuses"][status] = stats["statuses"].get(status, 0) + 1

    return stats


def run_scenario(api_token: str, scenario_id: str, base_url: str = BASE_URL) -> Dict[str, Any]:
    """Convenience wrapper to execute a scenario on demand.

    Parameters
    ----------
    api_token: str
        Personal API token for Make.com.
    scenario_id: str
        Identifier of the scenario to run.
    base_url: str, optional
        Base URL of the Make API. Defaults to ``https://api.make.com/v2``.
    """

    client = MakeClient(api_token=api_token, base_url=base_url)
    return client.run_scenario(scenario_id)
