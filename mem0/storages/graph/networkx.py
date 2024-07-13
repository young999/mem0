import networkx as nx
import sqlite3
import json
from typing import Any, Dict, List
from .base import BaseGraphStorage


class NetworkXGraphStorage(BaseGraphStorage):
    def __init__(self, db_path: str = 'graph_storage.db'):
        self.G = nx.Graph()
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self._load_graph_from_db()

    def disconnect(self):
        self._save_graph_to_db()
        if self.conn:
            self.conn.close()

    def add_node(self, node_id: str, properties: Dict[str, Any] = None):
        self.G.add_node(node_id, **properties or {})

    def add_edge(self, from_node: str, to_node: str, properties: Dict[str, Any] = None):
        self.G.add_edge(from_node, to_node, **properties or {})

    def get_node(self, node_id: str) -> Dict[str, Any]:
        if node_id not in self.G:
            raise KeyError(f"Node {node_id} not found in the graph")
        return dict(self.G.nodes[node_id])

    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        if node_id not in self.G:
            raise KeyError(f"Node {node_id} not found in the graph")
        return [{'id': neighbor, **dict(self.G.nodes[neighbor])} for neighbor in self.G.neighbors(node_id)]

    def query(self, query: str) -> List[Dict[str, Any]]:
        # This is a simple implementation. For complex queries, you might want to use a query language parser.
        if query.startswith("node:"):
            node_id = query.split(":", 1)[1]
            return [self.get_node(node_id)]
        elif query.startswith("neighbors:"):
            node_id = query.split(":", 1)[1]
            return self.get_neighbors(node_id)
        else:
            raise ValueError("Unsupported query format")

    def _load_graph_from_db(self):
        cursor = self.conn.cursor()

        # Create tables if they don't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS nodes
                          (id TEXT PRIMARY KEY, properties TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS edges
                          (from_node TEXT, to_node TEXT, properties TEXT,
                           PRIMARY KEY (from_node, to_node))''')

        # Load nodes
        cursor.execute("SELECT id, properties FROM nodes")
        for node_id, properties in cursor.fetchall():
            self.G.add_node(node_id, **json.loads(properties))

        # Load edges
        cursor.execute("SELECT from_node, to_node, properties FROM edges")
        for from_node, to_node, properties in cursor.fetchall():
            self.G.add_edge(from_node, to_node, **json.loads(properties))

    def _save_graph_to_db(self):
        cursor = self.conn.cursor()
        # Clear existing data
        cursor.execute("DELETE FROM nodes")
        cursor.execute("DELETE FROM edges")
        # Save nodes
        node_data = [(node, json.dumps(data)) for node, data in self.G.nodes(data=True)]
        cursor.executemany("INSERT INTO nodes VALUES (?, ?)", node_data)
        # Save edges
        edge_data = [(u, v, json.dumps(data)) for u, v, data in self.G.edges(data=True)]
        cursor.executemany("INSERT INTO edges VALUES (?, ?, ?)", edge_data)
        self.conn.commit()
