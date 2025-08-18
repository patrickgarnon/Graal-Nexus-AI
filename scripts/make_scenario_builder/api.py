"""Wrapper for the Make.com API."""

from __future__ import annotations

from . import _requests as requests


class MakeAPI:
    """Minimal wrapper around the Make.com REST API.

    Parameters
    ----------
    api_key: str
        API key used for authenticating with Make.com.
    base_url: str, optional
        Base URL of the Make.com API. Defaults to ``https://api.make.com/v2``.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.make.com/v2"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    # ------------------------------------------------------------------
    @property
    def headers(self) -> dict:
        """Return default headers for API requests."""

        return {"Authorization": f"Bearer {self.api_key}"}

    # ------------------------------------------------------------------
    def create_scenario(self, data: dict) -> dict:
        """Create a scenario."""

        response = requests.post(
            f"{self.base_url}/scenarios", headers=self.headers, json=data
        )
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    def read_scenario(self, scenario_id: int | str) -> dict:
        """Retrieve information about a scenario."""

        response = requests.get(
            f"{self.base_url}/scenarios/{scenario_id}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    def update_scenario(self, scenario_id: int | str, data: dict) -> dict:
        """Update a scenario."""

        response = requests.put(
            f"{self.base_url}/scenarios/{scenario_id}",
            headers=self.headers,
            json=data,
        )
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    def run_scenario(self, scenario_id: int | str) -> dict:
        """Execute a scenario on Make.com."""

        response = requests.post(
            f"{self.base_url}/scenarios/{scenario_id}/run", headers=self.headers
        )
        response.raise_for_status()
        return response.json()
