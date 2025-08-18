"""Agent definitions and loader."""

from dataclasses import dataclass
from typing import Dict, Any
import json


@dataclass
class Agent:
    """Simple agent representation."""

    name: str
    config: Dict[str, Any]

    def act(self, message: str) -> str:
        """Return a response for the given message."""
        return f"{self.name} received: {message}"


def load_agents(path: str) -> Dict[str, Agent]:
    """Load agent definitions from a JSON config file."""
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    agents = {
        entry["name"]: Agent(entry["name"], entry)
        for entry in data.get("agents", [])
    }
    return agents
