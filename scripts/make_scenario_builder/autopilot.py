"""Automatically tune and run Make.com scenarios."""

from __future__ import annotations

from typing import Iterable

from .builder import run_scenario, update_scenario


def run_autopilot(
    api,
    scenario_id: int | str,
    adjustments: Iterable[dict],
    max_attempts: int = 3,
) -> dict:
    """Run a scenario and apply adjustments on failure.

    Parameters
    ----------
    api:
        Instance of :class:`~scripts.make_scenario_builder.api.MakeAPI`.
    scenario_id:
        ID of the scenario to run.
    adjustments:
        Iterable of dictionaries to apply via :func:`update_scenario` when the
        scenario does not report success.
    max_attempts:
        Maximum number of times to run the scenario.
    """

    result: dict | None = None
    attempts = 0
    adj_iter = iter(adjustments)

    while attempts < max_attempts:
        attempts += 1
        result = run_scenario(api, scenario_id)
        if result.get("status") == "success":
            break
        try:
            update = next(adj_iter)
        except StopIteration:
            continue
        update_scenario(api, scenario_id, update)

    return result or {}
