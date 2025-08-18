from __future__ import annotations

import argparse
from pathlib import Path

from src import config
from src.agents import Agent
from src.scenarios import Scenario
from src.scheduler import Scheduler


def list_available(directory: Path) -> None:
    for item in directory.glob("*.json"):
        print(item.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Orchestrate agents and scenarios")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List available agents or scenarios")
    list_parser.add_argument("target", choices=["agents", "scenarios"], help="What to list")

    run_parser = subparsers.add_parser("run", help="Run a scenario with an agent")
    run_parser.add_argument("agent", help="Agent JSON filename")
    run_parser.add_argument("scenario", help="Scenario JSON filename")

    args = parser.parse_args()

    if args.command == "list":
        if args.target == "agents":
            list_available(config.AGENTS_DIR)
        else:
            list_available(config.SCENARIOS_DIR)
    elif args.command == "run":
        agent_path = config.AGENTS_DIR / args.agent
        scenario_path = config.SCENARIOS_DIR / args.scenario
        agent = Agent.from_file(agent_path)
        scenario = Scenario.from_file(scenario_path)
        scheduler = Scheduler(agent=agent, scenarios=[scenario])
        scheduler.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
