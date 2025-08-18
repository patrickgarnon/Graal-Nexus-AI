import logging
from typing import Any, Callable, Dict, List, Optional

import requests


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
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )
        self.logger = logging.getLogger(self.__class__.__name__)

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

    def run_scenario(self, scenario_id: str) -> Dict:
        """Trigger execution of the specified scenario and return its result.

        Args:
            scenario_id: Identifier of the scenario to run.

        Returns:
            Parsed JSON response from the API or an error dictionary.
        """
        url = f"{self.base_url}/v2/scenarios/{scenario_id}/run"
        try:
            response = self.session.post(url)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exc:  # pragma: no cover - network dependency
            return {"error": f"Error running scenario: {exc.response.text if exc.response else exc}"}  # pragma: no cover
        except requests.RequestException as exc:  # pragma: no cover - network dependency
            return {"error": f"Error running scenario: {exc}"}  # pragma: no cover

    def auto_pilot(
        self,
        scenario_id: str,
        metrics_fn: Callable[[Dict[str, Any]], float],
        *,
        threshold: float = 1.0,
        max_iterations: int = 5,
        adjustments: Optional[
            List[Callable[[str, float, Dict[str, Any]], Optional[Dict[str, Any]]]]
        ] = None,
    ) -> List[Dict[str, Any]]:
        """Run a scenario repeatedly, tuning it based on metrics.

        The scenario is executed and evaluated with ``metrics_fn``.  If the
        resulting metric is below ``threshold`` and adjustment strategies are
        provided, each strategy may return a patch to apply via
        :meth:`modify_scenario`.  Execution stops once the threshold is met or
        ``max_iterations`` is reached.

        Returns a history list containing the metric and raw result for each
        iteration, which is useful for auditing and debugging.
        """

        history: List[Dict[str, Any]] = []
        for iteration in range(1, max_iterations + 1):
            self.logger.info("Starting iteration %s for scenario %s", iteration, scenario_id)
            result = self.run_scenario(scenario_id)
            metric = metrics_fn(result)
            self.logger.info("Iteration %s metric: %s", iteration, metric)
            history.append(
                {
                    "iteration": iteration,
                    "scenario_id": scenario_id,
                    "metric": metric,
                    "result": result,
                }
            )
            if metric >= threshold:
                self.logger.info(
                    "Threshold %.2f reached with metric %.2f; stopping.", threshold, metric
                )
                break
            if adjustments:
                for strategy in adjustments:
                    patch = strategy(scenario_id, metric, result)
                    if patch:
                        self.logger.debug(
                            "Applying adjustment via %s: %s",
                            getattr(strategy, "__name__", str(strategy)),
                            patch,
                        )
                        self.modify_scenario(scenario_id, patch)
        return history
