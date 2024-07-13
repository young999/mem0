from abc import ABC, abstractmethod
from typing import Any, Dict, List
from mem0.storages.base import BaseStorage


class BaseGraphStorage(BaseStorage):
    @abstractmethod
    def add_node(self, node_id: str, properties: Dict[str, Any] = None):
        """Add a node to the graph."""
        pass

    @abstractmethod
    def add_edge(self, from_node: str, to_node: str, properties: Dict[str, Any] = None):
        """Add an edge between two nodes in the graph."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Dict[str, Any]:
        """Retrieve a node from the graph."""
        pass

    @abstractmethod
    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        """Get the neighbors of a given node."""
        pass

    @abstractmethod
    def query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a query on the graph."""
        pass
