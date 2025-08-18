import json
from pathlib import Path
from typing import Dict, Any

class App:
    """Central application loader for agents, scenarios and prompts."""

    def __init__(self, base_path: Path | None = None) -> None:
        # Base path is the directory containing the package folders
        self.base_path = base_path or Path(__file__).resolve().parent.parent

    def _load_json_dir(self, directory: Path) -> Dict[str, Any]:
        """Load all JSON files from a directory."""
        data: Dict[str, Any] = {}
        for path in directory.glob("*.json"):
            with path.open("r", encoding="utf-8") as fh:
                data[path.stem] = json.load(fh)
        return data

    def load_agents(self) -> Dict[str, Any]:
        """Return all available agents."""
        return self._load_json_dir(self.base_path / "agents")

    def load_scenarios(self) -> Dict[str, Any]:
        """Return all available scenarios."""
        return self._load_json_dir(self.base_path / "scenarios")

    def load_prompts(self) -> Dict[str, str]:
        """Return all text prompts."""
        prompts: Dict[str, str] = {}
        for path in (self.base_path / "prompts").glob("*.txt"):
            prompts[path.stem] = path.read_text(encoding="utf-8")
        return prompts
