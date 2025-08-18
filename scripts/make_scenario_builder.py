import logging
from typing import Any, Callable, Dict, List, Optional


class MakeScenarioBuilder:
    """Utility class to orchestrate Make.com scenarios.

    This builder provides an ``auto_pilot`` helper that can automatically
    iterate on a scenario until a desired metric threshold is reached or a
    maximum number of iterations is exceeded.  The ``metrics_fn`` allows
    callers to plug in custom evaluation logic.
    """

    def __init__(self, client: Any):
        """Parameters
        ----------
        client:
            Object exposing a ``run_scenario(scenario_id: str)`` method used to
            execute scenarios on the Make platform.  It can be an SDK client or
            any wrapper implementing the expected API.
        """
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Execute a scenario and return the raw result.

        The default implementation simply delegates to ``self.client``.  It can
        be overridden in subclasses for custom behaviour.
        """
        return self.client.run_scenario(scenario_id)

    def auto_pilot(
        self,
        scenario_id: str,
        metrics_fn: Callable[[Dict[str, Any]], float],
        *,
        threshold: float = 1.0,
        max_iterations: int = 5,
        adjustments: Optional[List[Callable[[str, float, Dict[str, Any]], str]]] = None,
    ) -> List[Dict[str, Any]]:
        """Automatically iterate on a scenario until it meets a metric threshold.

        Parameters
        ----------
        scenario_id:
            Identifier of the scenario to execute.
        metrics_fn:
            Callable receiving the scenario result and returning a numeric score.
        threshold:
            Minimum score required to stop the loop.
        max_iterations:
            Maximum number of iterations to attempt before giving up.
        adjustments:
            Optional list of callables used to update the ``scenario_id`` after
            each iteration.  Each strategy receives the current ``scenario_id``,
            the computed metric and the raw result.  It must return the new
            ``scenario_id`` to use for the next iteration.

        Returns
        -------
        List[Dict[str, Any]]
            Historical log of each iteration containing the scenario identifier,
            metrics and raw result.
        """
        history: List[Dict[str, Any]] = []
        for iteration in range(1, max_iterations + 1):
            self.logger.info("Starting iteration %s for scenario %s", iteration, scenario_id)
            result = self.run_scenario(scenario_id)
            metric = metrics_fn(result)
            self.logger.info("Iteration %s metrics: %s", iteration, metric)
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
                    new_scenario_id = strategy(scenario_id, metric, result)
                    if new_scenario_id != scenario_id:
                        self.logger.debug(
                            "Strategy %s updated scenario %s -> %s",
                            getattr(strategy, "__name__", str(strategy)),
                            scenario_id,
                            new_scenario_id,
                        )
                        scenario_id = new_scenario_id
        return history
