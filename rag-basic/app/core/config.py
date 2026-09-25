from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Nugen API
    NUGEN_API_KEY: str
    NUGEN_BASE_URL: str = "https://api.nugen.in/inference"
    NUGEN_EMBED_MODEL: str = "nugen-flash-embed"
    NUGEN_CHAT_MODEL: str = "nugen-flash-instruct"

    # Qdrant
    QDRANT_COLLECTION: str = "rag_documents"
    VECTOR_SIZE: int = 768

    # RAG
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    class Config:
        env_file = ".env"


settings = Settings()
