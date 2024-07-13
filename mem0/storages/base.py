from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

class BaseStorage(ABC):
    @abstractmethod
    def connect(self):
        """Establish a connection to the storage."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the connection to the storage."""
        pass
