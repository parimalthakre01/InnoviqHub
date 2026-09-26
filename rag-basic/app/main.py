from fastapi import FastAPI, HTTPException
from app.models.schemas import AddData, IngestResponse, QueryRequest, QueryResponse, RetrievedChunk
from app.services.rag_pipeline import ingest_document, query_rag
from app.services.vector_store import client as qdrant_client
from app.core.config import settings

app = FastAPI(title="RAG Basic", description="RAG with Qdrant + Nugen", version="0.1.0")

# RAG application : document collection --> extract text from document --> divide into chunks --> create embeddings for each chunks --> store in vector database --> ask question --> retrieve data -> pass it to LLM for answer generation

@app.get("/health")
def health():
    return {"status": "ok"}

# Types of HTTP request: GET POST PUT DELETE 
# Define endpoint: Request and Response
# Request --> data from user either compulsory or optional

# Response --> data from server either compulsory or optional

@app.post("/api/v1/addData/", response_model=IngestResponse, tags=["ingest"])
def ingest(request: AddData):
    count = ingest_document(request.text, request.metadata or {}) # function to add documents
    return IngestResponse(message="Document added successfully", chunks_stored=count)


@app.post("/api/v1/query/", response_model=QueryResponse, tags=["query"])
def query(request: QueryRequest):
    result = query_rag(request.question, request.top_k)
    return QueryResponse(
        question=request.question,
        answer=result["answer"],
        sources=[RetrievedChunk(**s) for s in result["sources"]],
    )


@app.get("/api/v1/documents/", tags=["documents"])
def list_documents():
    result = qdrant_client.scroll(
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
