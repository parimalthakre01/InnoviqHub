from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Nugen API
    NUGEN_API_KEY: str
    NUGEN_BASE_URL: str = "https://api.nugen.in/api/v3/inference"
    NUGEN_EMBED_MODEL: str = "qwen3-embedding-8b"
    NUGEN_CHAT_MODEL: str = "qwen-v2p5-0p5b-instruct"

    # Qdrant
    QDRANT_URL: str = ""
    QDRANT_COLLECTION: str = "rag_documents"
    VECTOR_SIZE: int = 4096

    # RAG
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    class Config:
        env_file = ".env"


settings = Settings()
