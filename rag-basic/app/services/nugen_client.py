import json
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
    with httpx.Client(timeout=120.0) as client:
        with client.stream(
            "POST",
            f"{settings.NUGEN_BASE_URL}/chat/completions",
            headers=HEADERS,
            json={
                "model": settings.NUGEN_CHAT_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "stream": True,
            },
        ) as response:
            response.raise_for_status()
            result = []
            for line in response.iter_lines():
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                chunk = json.loads(data)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    result.append(delta)
            return "".join(result)
