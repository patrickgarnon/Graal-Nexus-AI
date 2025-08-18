import argparse
import logging

from logging_utils import setup_logging, get_logger


def main() -> None:
    parser = argparse.ArgumentParser(description="Graal Nexus AI runner")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug output",
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging(level)

    if args.verbose:
        logger.debug("Verbose logging enabled")

    logger.info("Scenario start")
    try:
        # Placeholder for scenario logic
        logger.info("Scenario complete")
    except Exception:  # noqa: BLE001
        logger.exception("Scenario failed")
        raise


if __name__ == "__main__":
    main()
