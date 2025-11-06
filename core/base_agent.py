from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Abstract interface that all agents must implement."""

    @abstractmethod
    async def chat(self, message: str, dialog_id: str | None = None) -> str:
        """Accept a message and return agent response."""
