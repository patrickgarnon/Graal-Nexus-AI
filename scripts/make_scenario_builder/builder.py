"""Utilities for composing Make.com scenarios."""

from __future__ import annotations

from .api import MakeAPI


def create_scenario(api: MakeAPI, name: str, modules: list | None = None) -> dict:
    """Create a new scenario with an optional list of modules."""

    payload = {"name": name}
    if modules:
        payload["modules"] = modules
    return api.create_scenario(payload)


def clone_scenario(api: MakeAPI, scenario_id: int | str) -> dict:
    """Clone an existing scenario."""

    original = api.read_scenario(scenario_id)
    original.pop("id", None)
    original["name"] = f"{original.get('name', 'scenario')} (clone)"
    return api.create_scenario(original)


def update_scenario(api: MakeAPI, scenario_id: int | str, updates: dict) -> dict:
    """Update a scenario with the provided data."""

    return api.update_scenario(scenario_id, updates)


def run_scenario(api: MakeAPI, scenario_id: int | str) -> dict:
    """Run a scenario."""

    return api.run_scenario(scenario_id)


def chain_http_modules(api: MakeAPI, scenario_id: int | str, urls: list[str]) -> dict:
    """Replace the scenario's modules with a chain of HTTP modules calling ``urls``."""

    modules = [{"type": "http", "url": url} for url in urls]
    return update_scenario(api, scenario_id, {"modules": modules})
