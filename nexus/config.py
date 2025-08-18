"""Global configuration for Nexus utilities."""
from dataclasses import dataclass, field
from typing import Tuple, Type


@dataclass
class RetryConfig:
    """Configuration options for the :func:`retry` decorator."""
    enabled: bool = True
    max_attempts: int = 3
    backoff_factor: float = 0.5
    exceptions: Tuple[Type[BaseException], ...] = field(
        default_factory=lambda: (Exception,)
    )


# Global instance used by the retry decorator
retry_config = RetryConfig()
