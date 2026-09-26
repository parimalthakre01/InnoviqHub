import app.services.nugen_client as nugen
import app.services.vector_store as vs
from app.utils.chunker import chunk_text
from app.core.config import settings

SYSTEM_PROMPT = """You are a helpful assistant. Answer the user's question using only
the provided context. If the context does not contain enough information, say so."""

# function is used to add data in qdrant db
def ingest_document(text: str, metadata: dict = {}) -> int:
    chunks = chunk_text(text) # text is received from users as a request parameter
    for chunk in chunks:
        vector = nugen.embed(chunk)
        paylaod = {"text": chunk, **metadata}
        vs.upsert([vector], [paylaod])  
    return len(chunks)


def query_rag(question: str, top_k: int = None) -> dict:
    # top_k = top_k or settings.TOP_K
    query_vector = nugen.embed(question)
    retrieved = vs.search(query_vector, top_k)

    filtered = [r for r in retrieved if r["score"] >= settings.SIMILARITY_THRESHOLD]
    context = "\n\n".join(r["text"] for r in filtered) or "No relevant context found."

    user_message = f"Context:\n{context}\n\nQuestion: {question}"
    answer = nugen.chat(SYSTEM_PROMPT, user_message)

    return {"answer": answer, "sources": filtered}
