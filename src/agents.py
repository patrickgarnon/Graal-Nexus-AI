from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Agent:
    """Simple representation of an Agent loaded from a JSON file."""

    name: str
    description: str

    @classmethod
    def from_file(cls, path: Path) -> "Agent":
        """Load an agent definition from a JSON file."""
        with path.open("r", encoding="utf-8") as fh:
            data: dict[str, Any] = json.load(fh)
        return cls(name=data.get("agent_name", "Unnamed Agent"), description=data.get("description", ""))

    def act(self) -> None:
        """Trigger the agent's action. For now, simply prints its description."""
        print(f"[AGENT] {self.name}: {self.description}")
