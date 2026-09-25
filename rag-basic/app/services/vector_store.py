from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
import uuid
from app.core.config import settings


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(":memory:")
        self.collection = settings.QDRANT_COLLECTION
        self._init_collection()

    def _init_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=settings.VECTOR_SIZE,
                distance=Distance.COSINE,  # cosine similarity
            ),
        )

    def upsert(self, vectors: list[list[float]], payloads: list[dict]):
        points = [
            PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload)
            for vec, payload in zip(vectors, payloads)
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )
        return [
            {"text": r.payload.get("text", ""), "score": r.score, "metadata": r.payload}
            for r in results
        ]


vector_store = VectorStore()
