import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock

from make_scenario_builder import MakeScenarioBuilder


def test_auto_pilot_iterates_and_applies_adjustments():
    builder = MakeScenarioBuilder("token", "https://api.make.com")
    builder.run_scenario = MagicMock(side_effect=[{"score": 0.2}, {"score": 1.3}])
    builder.modify_scenario = MagicMock(return_value="ok")

    def metrics_fn(result):
        return result["score"]

    def adjustment(scenario_id, metric, result):
        return {"tuned": metric}

    history = builder.auto_pilot(
        "42",
        metrics_fn,
        threshold=1.0,
        max_iterations=5,
        adjustments=[adjustment],
    )

    assert builder.run_scenario.call_count == 2
    builder.modify_scenario.assert_called_once_with("42", {"tuned": 0.2})
    assert len(history) == 2
    assert history[-1]["metric"] >= 1.0
