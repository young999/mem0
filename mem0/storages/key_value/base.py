from abc import ABC, abstractmethod
from typing import Any, Dict, List
from mem0.storages.base import BaseStorage


class BaseKeyValueStorage(BaseStorage):
    @abstractmethod
    def set(self, key: str, value: Any):
        """Set a key-value pair."""
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        """Get the value for a given key."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Delete a key-value pair."""
        pass

    @abstractmethod
    def keys(self) -> List[str]:
        """Get all keys in the storage."""
        pass
