from abc import ABC, abstractmethod


class Agent(ABC):
    """Base interface for all agents."""

    @abstractmethod
    def perform(self, *args, **kwargs):
        """Execute the agent's main behaviour."""
        raise NotImplementedError
