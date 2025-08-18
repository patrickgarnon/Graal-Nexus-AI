from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .agents import Agent
from .scenarios import Scenario


@dataclass
class Scheduler:
    """Basic scheduler to run scenarios with a given agent."""

    agent: Agent
    scenarios: Iterable[Scenario]

    def run(self) -> None:
        for scenario in self.scenarios:
            scenario.execute(self.agent)
