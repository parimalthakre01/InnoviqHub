from fastapi import APIRouter
from app.api.routes import ingest, query, documents

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(ingest.router)
api_router.include_router(query.router)
api_router.include_router(documents.router)
