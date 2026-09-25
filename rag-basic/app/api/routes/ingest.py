from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse
from app.services.rag_pipeline import ingest_document

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    try:
        count = await ingest_document(request.text, request.metadata or {})
        return IngestResponse(message="Document ingested successfully", chunks_stored=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
