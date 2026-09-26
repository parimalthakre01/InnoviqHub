import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.core.config import settings

if settings.QDRANT_URL:
    client = QdrantClient(url=settings.QDRANT_URL)
else:
    client = QdrantClient(":memory:")

existing = [c.name for c in client.get_collections().collections]
if settings.QDRANT_COLLECTION in existing:
    client.delete_collection(settings.QDRANT_COLLECTION)
client.create_collection(
    collection_name=settings.QDRANT_COLLECTION,
    vectors_config=VectorParams(size=settings.VECTOR_SIZE, distance=Distance.COSINE),
)


def upsert(vectors: list[list[float]], payloads: list[dict]):
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload)
        for vec, payload in zip(vectors, payloads)
    ]
    client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)


def search(query_vector: list[float], top_k: int) -> list[dict]:
    results = client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points
    return [
        {"text": r.payload.get("text", ""), "score": r.score, "metadata": r.payload}
        for r in results
    ]
