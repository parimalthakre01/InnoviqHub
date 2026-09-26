from fastapi import APIRouter
from app.services.vector_store import vector_store
from app.core.config import settings

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/")
def list_documents():
    result = vector_store.client.scroll(
        collection_name=settings.QDRANT_COLLECTION,
        with_payload=True,
        with_vectors=False,
        limit=100,
    )
    points = result[0]
    return {
        "total": len(points),
        "documents": [
            {"id": str(p.id), "payload": p.payload}
            for p in points
        ],
    }
