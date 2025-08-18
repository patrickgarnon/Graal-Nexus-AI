from abc import ABC, abstractmethod


class Scenario(ABC):
    """Base interface for all scenarios."""

    @abstractmethod
    def setup(self, *args, **kwargs):
        """Prepare the scenario before agents run."""
        raise NotImplementedError
