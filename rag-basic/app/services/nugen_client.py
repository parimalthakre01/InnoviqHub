import httpx
from app.core.config import settings


class NugenClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.NUGEN_API_KEY}",
            "Content-Type": "application/json",
        }

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.NUGEN_BASE_URL}/embeddings",
                headers=self.headers,
                json={"model": settings.NUGEN_EMBED_MODEL, "input": text},
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]

    async def chat(self, system_prompt: str, user_message: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.NUGEN_BASE_URL}/chat/completions",
                headers=self.headers,
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


nugen_client = NugenClient()
