from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, RetrievedChunk
from app.services.rag_pipeline import query_rag

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = await query_rag(request.question, request.top_k)
        return QueryResponse(
            question=request.question,
            answer=result["answer"],
            sources=[RetrievedChunk(**s) for s in result["sources"]],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
