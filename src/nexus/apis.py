"""Simple API integration placeholder."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class APIIntegration:
    """Represent an external API integration."""

    name: str
    base_url: str

    def call(self, endpoint: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Mock an API call.

        In a real implementation, this would perform an HTTP request.
        """
        return {"endpoint": endpoint, "params": params or {}, "base_url": self.base_url}
