"""Scenario management and execution."""

from dataclasses import dataclass
from typing import List, Dict
import json
from .agents import Agent


@dataclass
class Step:
    agent: str
    message: str


@dataclass
class Scenario:
    name: str
    steps: List[Step]

    def run(self, agents: Dict[str, Agent]) -> None:
        """Execute each step using the provided agents."""
        for step in self.steps:
            agent = agents.get(step.agent)
            if agent is None:
                raise KeyError(f"Agent '{step.agent}' not found")
            response = agent.act(step.message)
            print(response)


def load_scenarios(path: str) -> Dict[str, Scenario]:
    """Load scenarios from a JSON config file."""
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    scenarios: Dict[str, Scenario] = {}
    for entry in data.get("scenarios", []):
        steps = [Step(**step) for step in entry.get("steps", [])]
        scenario = Scenario(name=entry["name"], steps=steps)
        scenarios[scenario.name] = scenario
    return scenarios
