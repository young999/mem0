import json
from typing import Any, List
from .base import BaseKeyValueStorage


class DefaultKeyValueStorage(BaseKeyValueStorage):
    def __init__(self, file_path: str = 'kv_storage.json'):
        self.file_path = file_path
        self.store = {}

    def connect(self):
        try:
            with open(self.file_path, 'r') as f:
                self.store = json.load(f)
        except FileNotFoundError:
            self.store = {}

    def disconnect(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.store, f, indent=2)

    def set(self, key: str, value: Any):
        self.store[key] = value

    def get(self, key: str) -> Any:
        if key not in self.store:
            raise KeyError(f"Key '{key}' not found in the store")
        return self.store[key]

    def delete(self, key: str):
        if key not in self.store:
            raise KeyError(f"Key '{key}' not found in the store")
        del self.store[key]

    def keys(self) -> List[str]:
        return list(self.store.keys())

    def clear(self):
        """Clear all key-value pairs from the store."""
        self.store.clear()

    def update(self, other_dict: dict):
        """Update the store with key-value pairs from another dictionary."""
        self.store.update(other_dict)

    def items(self):
        """Return a view of the store's items."""
        return self.store.items()

    def values(self):
        """Return a view of the store's values."""
        return self.store.values()

    def get_or_default(self, key: str, default: Any = None) -> Any:
        """Get a value for a key, or return a default if the key doesn't exist."""
        return self.store.get(key, default)

    def __len__(self):
        """Return the number of items in the store."""
        return len(self.store)

    def __contains__(self, key):
        """Check if a key exists in the store."""
        return key in self.store

    def __iter__(self):
        """Return an iterator over the keys of the store."""
        return iter(self.store)
