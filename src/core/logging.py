"""Utility for application logging with configurable verbosity.

This module sets up logging for the project. Logs are emitted to both
standard output and a file located at ``logs/graal.log``. By default the
logging level is ``INFO`` but it can be switched to ``DEBUG`` mode by
passing a ``--verbose`` flag when executing the module.
"""

from __future__ import annotations

import argparse
import logging as _logging
from pathlib import Path
import sys

LOG_FILE_PATH = Path("logs/graal.log")


def setup_logging(verbose: bool = False) -> _logging.Logger:
    """Configure and return the application logger.

    Parameters
    ----------
    verbose:
        When ``True`` sets the logging level to ``DEBUG``; otherwise
        ``INFO`` is used.
    """
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    level = _logging.DEBUG if verbose else _logging.INFO

    logger = _logging.getLogger("graal")
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicate logs in interactive sessions
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = _logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    stream_handler = _logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = _logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure Graal logging")
    parser.add_argument(
        "--verbose", action="store_true", help="Enable debug logging"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    logger = setup_logging(args.verbose)
    logger.info("Logging initialized")
    logger.debug("Verbose logging enabled")


if __name__ == "__main__":
    main()
