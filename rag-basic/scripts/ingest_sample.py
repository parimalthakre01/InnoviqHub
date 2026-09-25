"""One-off script to ingest a sample document via the API."""
import asyncio
import httpx

SAMPLE_TEXT = """
FastAPI is a modern, fast (high-performance), web framework for building APIs with
Python based on standard Python type hints. It is one of the fastest Python frameworks
available, on par with NodeJS and Go. FastAPI uses Pydantic for data validation and
settings management.
"""


async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/v1/ingest/",
            json={"text": SAMPLE_TEXT, "metadata": {"source": "sample"}},
        )
        print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
