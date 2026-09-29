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
    question = nugen.enhance_query(question)
    # generate vectors for question
    query_vector = nugen.embed(question)
    retrieved = vs.search(query_vector, top_k)
    # add reranker here
    # filtered = [r for r in retrieved if r["score"] >= settings.SIMILARITY_THRESHOLD]
    context = "\n\n".join(r["text"] for r in retrieved) or "No relevant context found."
    print(f"Retrieved {len(retrieved)} chunks for question: {question}")
    user_message = f"Context:\n{context}\n\nQuestion: {question}"
    print(f"User message for LLM:\n{user_message}")
    answer = nugen.chat(SYSTEM_PROMPT, user_message)

    return {"answer": answer, "sources": retrieved}
