"""Command line interface for triggering Make scenarios concurrently."""
from __future__ import annotations

import argparse
import asyncio
from typing import Sequence

from .core.executor import run_scenarios


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "api_token", help="Authentication token for the Make API"
    )
    parser.add_argument(
        "scenario_ids",
        nargs="+",
        help="One or more scenario identifiers to trigger",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Maximum number of worker threads for concurrent execution",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    results = asyncio.run(
        run_scenarios(
            api_token=args.api_token,
            scenario_ids=args.scenario_ids,
            max_workers=args.max_workers,
        )
    )
    for res in results:
        scenario = res.get("scenario", "?")
        status = res.get("status", "unknown")
        print(f"Scenario {scenario} finished with status {status}.")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
