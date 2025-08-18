import importlib
import json
from pathlib import Path
from typing import List, Type

from src.interfaces import Agent, Scenario


class AutopilotEngine:
    """Engine orchestrating agents and scenarios based on JSON configs."""

    def __init__(self, config_dir: str = "config") -> None:
        self.config_dir = Path(config_dir)
        self.agents: List[Agent] = []
        self.scenarios: List[Scenario] = []
        self._load_configs()

    def _load_configs(self) -> None:
        """Load agent and scenario definitions from JSON files."""
        if not self.config_dir.exists():
            return
        for path in self.config_dir.glob("*.json"):
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            for agent_conf in data.get("agents", []):
                self.agents.append(self._instantiate(agent_conf))
            for scenario_conf in data.get("scenarios", []):
                self.scenarios.append(self._instantiate(scenario_conf))

    def _instantiate(self, conf: dict):
        cls = self._import_from_path(conf["path"])
        params = conf.get("params", {})
        return cls(**params)

    def _import_from_path(self, dotted_path: str) -> Type:
        module_name, class_name = dotted_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def run(self) -> None:
        for scenario in self.scenarios:
            scenario.setup()
            for agent in self.agents:
                agent.perform(scenario)
