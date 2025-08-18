import logging

LOGGER_NAME = "graal_nexus"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure root logger and return the central logger.

    Parameters
    ----------
    level: int
        Logging level to configure. Defaults to INFO.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(LOGGER_NAME)


def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """Retrieve a logger with the given name."""
    return logging.getLogger(name)
