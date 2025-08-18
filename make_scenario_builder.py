import requests
from typing import Dict


class MakeScenarioBuilder:
    """Client for building and controlling Make.com scenarios."""

    def __init__(self, api_key: str, base_url: str) -> None:
        """Initialize the builder with API credentials.

        Args:
            api_key: Make.com API key.
            base_url: Base URL of the Make.com workspace API.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def create_scenario(self, structure: Dict) -> str:
        """Create a new scenario from the given structure.

        Args:
            structure: Scenario definition payload.

        Returns:
            The identifier of the created scenario or an error message.
        """
        url = f"{self.base_url}/v2/scenarios"
        try:
            response = self.session.post(url, json=structure)
            response.raise_for_status()
            data = response.json()
            return data.get("id") or data.get("_id", "")
        except requests.HTTPError as exc:  # pragma: no cover - network dependency
            return f"Error creating scenario: {exc.response.text if exc.response else exc}"  # pragma: no cover
        except requests.RequestException as exc:  # pragma: no cover - network dependency
            return f"Error creating scenario: {exc}"  # pragma: no cover

    def clone_scenario(self, scenario_id: str) -> str:
        """Clone an existing scenario.

        Args:
            scenario_id: Identifier of the scenario to clone.

        Returns:
            Identifier of the new scenario or an error message.
        """
        url = f"{self.base_url}/v2/scenarios/{scenario_id}/clone"
        try:
            response = self.session.post(url)
            response.raise_for_status()
            data = response.json()
            return data.get("id") or data.get("_id", "")
        except requests.HTTPError as exc:  # pragma: no cover - network dependency
            return f"Error cloning scenario: {exc.response.text if exc.response else exc}"  # pragma: no cover
        except requests.RequestException as exc:  # pragma: no cover - network dependency
            return f"Error cloning scenario: {exc}"  # pragma: no cover

    def modify_scenario(self, scenario_id: str, patch: Dict) -> str:
        """Update an existing scenario with the provided patch.

        Args:
            scenario_id: Identifier of the scenario to modify.
            patch: Partial scenario definition to apply.

        Returns:
            A success or error message.
        """
        url = f"{self.base_url}/v2/scenarios/{scenario_id}"
        try:
            response = self.session.patch(url, json=patch)
            response.raise_for_status()
            return "Scenario updated successfully"
        except requests.HTTPError as exc:  # pragma: no cover - network dependency
            return f"Error modifying scenario: {exc.response.text if exc.response else exc}"  # pragma: no cover
        except requests.RequestException as exc:  # pragma: no cover - network dependency
            return f"Error modifying scenario: {exc}"  # pragma: no cover

    def run_scenario(self, scenario_id: str) -> str:
        """Trigger execution of the specified scenario.

        Args:
            scenario_id: Identifier of the scenario to run.

        Returns:
            A success or error message.
        """
        url = f"{self.base_url}/v2/scenarios/{scenario_id}/run"
        try:
            response = self.session.post(url)
            response.raise_for_status()
            return "Scenario run triggered"
        except requests.HTTPError as exc:  # pragma: no cover - network dependency
            return f"Error running scenario: {exc.response.text if exc.response else exc}"  # pragma: no cover
        except requests.RequestException as exc:  # pragma: no cover - network dependency
            return f"Error running scenario: {exc}"  # pragma: no cover
