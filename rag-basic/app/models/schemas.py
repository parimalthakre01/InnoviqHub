from pydantic import BaseModel
from typing import Optional


class IngestRequest(BaseModel):
    text: str
    metadata: Optional[dict] = {}


class IngestResponse(BaseModel):
    message: str
    chunks_stored: int


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5


class RetrievedChunk(BaseModel):
    text: str
    score: float
    metadata: dict


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[RetrievedChunk]
