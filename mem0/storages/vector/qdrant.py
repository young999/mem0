from typing import List, Tuple, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, FieldCondition, MatchValue, Range, Filter
from pydantic import BaseModel, Field
from ..base import BaseVectorStorage


class QdrantConfig(BaseModel):
    host: Optional[str] = Field(None, description="Host address for Qdrant server")
    port: Optional[int] = Field(None, description="Port for Qdrant server")
    path: Optional[str] = Field(None, description="Path for local Qdrant database")
    url: Optional[str] = Field(None, description="Full URL for Qdrant server")
    api_key: Optional[str] = Field(None, description="API key for Qdrant server")


class QdrantVectorStorage(BaseVectorStorage):
    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client = None

    def connect(self):
        params = {}
        if self.config.path:
            params["path"] = self.config.path
        if self.config.api_key:
            params["api_key"] = self.config.api_key
        if self.config.url:
            params["url"] = self.config.url
        if self.config.host and self.config.port:
            params["host"] = self.config.host
            params["port"] = self.config.port
        self.client = QdrantClient(**params)

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

    def add_vector(self, id: str, vector: List[float], metadata: Dict[str, Any] = None, collection_name: str = "default"):
        point = PointStruct(id=id, vector=vector, payload=metadata or {})
        self.client.upsert(collection_name=collection_name, points=[point])

    def get_vector(self, id: str, collection_name: str = "default") -> Tuple[List[float], Dict[str, Any]]:
        result = self.client.retrieve(collection_name=collection_name, ids=[id], with_payload=True, with_vectors=True)
        if not result:
            raise KeyError(f"Vector with id {id} not found")
        point = result[0]
        return point.vector, point.payload

    def search(self, query_vector: List[float], k: int = 10, collection_name: str = "default", filters: Dict[str, Any] = None) -> List[Tuple[str, float, Dict[str, Any]]]:
        query_filter = self._create_filter(filters) if filters else None
        hits = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=k
        )
        return [(hit.id, hit.score, hit.payload) for hit in hits]

    def delete_vector(self, id: str, collection_name: str = "default"):
        self.client.delete(collection_name=collection_name, points_selector=[id])

    def create_collection(self, name: str, vector_size: int, distance: Distance = Distance.COSINE):
        self.client.create_collection(
            collection_name=name,
            vectors_config={"size": vector_size, "distance": distance},
        )

    def _create_filter(self, filters: Dict[str, Any]) -> Filter:
        conditions = []
        for key, value in filters.items():
            if isinstance(value, dict) and "gte" in value and "lte" in value:
                conditions.append(FieldCondition(key=key, range=Range(gte=value["gte"], lte=value["lte"])))
            else:
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
        return Filter(must=conditions) if conditions else None

    def list_collections(self):
        return self.client.get_collections().collections

    def delete_collection(self, name: str):
        self.client.delete_collection(collection_name=name)

    def collection_info(self, name: str):
        return self.client.get_collection(collection_name=name)
