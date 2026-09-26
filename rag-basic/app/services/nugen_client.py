import httpx
from app.core.config import settings

HEADERS = {
    "Authorization": f"Bearer {settings.NUGEN_API_KEY}",
    "Content-Type": "application/json",
}


def embed(text: str) -> list[float]:
    with httpx.Client() as client:
        response = client.post(
            f"{settings.NUGEN_BASE_URL}/embeddings",
            headers=HEADERS,
            json={"model": settings.NUGEN_EMBED_MODEL, "input": text},
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]


def chat(system_prompt: str, user_message: str) -> str:
    with httpx.Client() as client:
        response = client.post(
            f"{settings.NUGEN_BASE_URL}/chat/completions",
            headers=HEADERS,
            json={
                "model": settings.NUGEN_CHAT_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
