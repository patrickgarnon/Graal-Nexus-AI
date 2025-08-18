from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .agents import Agent


@dataclass
class Scenario:
    """A scenario that can be executed by an Agent."""

    name: str
    goal: str

    @classmethod
    def from_file(cls, path: Path) -> "Scenario":
        """Load a scenario definition from a JSON file."""
        with path.open("r", encoding="utf-8") as fh:
            data: dict[str, Any] = json.load(fh)
        return cls(name=data.get("scenario_name", "Unnamed Scenario"), goal=data.get("goal", ""))

    def execute(self, agent: Agent) -> None:
        """Execute the scenario using the provided agent."""
        print(f"[SCENARIO] {self.name}: {self.goal}")
        agent.act()
