from app.services.nugen_client import nugen_client
from app.services.vector_store import vector_store
from app.utils.chunker import chunk_text
from app.core.config import settings

SYSTEM_PROMPT = """You are a helpful assistant. Answer the user's question using only
the provided context. If the context does not contain enough information, say so."""


async def ingest_document(text: str, metadata: dict = {}) -> int:
    chunks = chunk_text(text)
    vectors = [await nugen_client.embed(chunk) for chunk in chunks]
    payloads = [{"text": chunk, **metadata} for chunk in chunks]
    vector_store.upsert(vectors, payloads)
    return len(chunks)


async def query_rag(question: str, top_k: int = None) -> dict:
    top_k = top_k or settings.TOP_K
    query_vector = await nugen_client.embed(question)
    retrieved = vector_store.search(query_vector, top_k)

    filtered = [r for r in retrieved if r["score"] >= settings.SIMILARITY_THRESHOLD]
    context = "\n\n".join(r["text"] for r in filtered) or "No relevant context found."

    user_message = f"Context:\n{context}\n\nQuestion: {question}"
    answer = await nugen_client.chat(SYSTEM_PROMPT, user_message)

    return {"answer": answer, "sources": filtered}
