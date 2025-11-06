from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal

MessageRole = Literal["system", "user", "assistant"]


class BaseMemory(ABC):
    """Abstract memory API."""

    @abstractmethod
    async def append(self, dialog_id: str, role: str, text: str) -> None: ...

    @abstractmethod
    async def get_history(self, dialog_id: str, limit: int = 50) -> List[Dict[str, Any]]: ...


class InMemoryMemory(BaseMemory):
    """Simple in-memory history store for development/testing."""

    def __init__(self) -> None:
        self.store: Dict[str, List[Dict[str, str]]] = {}

    async def append(self, dialog_id: str, role: MessageRole, content: str) -> None:
        self.store.setdefault(dialog_id, []).append({"role": role, "content": content})

    async def get_history(self, dialog_id: str, limit: int = 50):
        return self.store.get(dialog_id, [])[-limit:]
