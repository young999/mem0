from abc import abstractmethod
from typing import Any, Dict, List, Tuple
from mem0.storages.base import BaseStorage


class BaseVectorStorage(BaseStorage):
    @abstractmethod
    def add_vector(self, id: str, vector: List[float], metadata: Dict[str, Any] = None):
        """Add a vector to the storage."""
        pass

    @abstractmethod
    def get_vector(self, id: str) -> Tuple[List[float], Dict[str, Any]]:
        """Retrieve a vector and its metadata by ID."""
        pass

    @abstractmethod
    def search(self, query_vector: List[float], k: int = 10) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for the k nearest vectors to the query vector."""
        pass

    @abstractmethod
    def delete_vector(self, id: str):
        """Delete a vector from the storage."""
        pass
