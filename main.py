"""Command line entry point for running Nexus scenarios."""

from pathlib import Path
import sys

# Ensure the src directory is on the path
ROOT = Path(__file__).parent
sys.path.append(str(ROOT / "src"))

from nexus.agents import load_agents
from nexus.scenarios import load_scenarios


CONFIG_DIR = ROOT / "config"


def main() -> None:
    agents = load_agents(CONFIG_DIR / "agents.json")
    scenarios = load_scenarios(CONFIG_DIR / "scenarios.json")

    for scenario in scenarios.values():
        print(f"Running scenario: {scenario.name}")
        scenario.run(agents)


if __name__ == "__main__":
    main()
