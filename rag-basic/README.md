# RAG Basic

A minimal Retrieval-Augmented Generation (RAG) API built with FastAPI, Qdrant (in-memory), and Nugen as the inference and embedding provider.

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Vector DB | Qdrant `:memory:` |
| Similarity | Cosine |
| Embeddings | Nugen (`nugen-flash-embed`) |
| LLM | Nugen (`nugen-flash-instruct`) |

## Project Structure

```
rag-basic/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   ├── router.py            # mounts all routes under /api/v1
│   │   └── routes/
│   │       ├── ingest.py        # POST /api/v1/ingest/
│   │       └── query.py         # POST /api/v1/query/
│   ├── core/
│   │   └── config.py            # settings via pydantic-settings + .env
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response schemas
│   ├── services/
│   │   ├── nugen_client.py      # async Nugen API client (embed + chat)
│   │   ├── vector_store.py      # Qdrant in-memory vector store
│   │   └── rag_pipeline.py      # ingest and query orchestration
│   └── utils/
│       └── chunker.py           # sliding-window text chunker
├── data/
│   ├── raw/                     # place source documents here
│   └── processed/
├── scripts/
│   └── ingest_sample.py         # quick smoke-test ingest script
├── tests/
│   ├── unit/test_chunker.py
│   └── integration/test_api.py
├── .env.example
└── requirements.txt
```

## Setup

```bash
# 1. Clone and enter the project
cd rag-basic

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set your NUGEN_API_KEY
```

## Running

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## API Endpoints

### `POST /api/v1/ingest/`

Chunks a document and stores embeddings in Qdrant.

**Request:**
```json
{
  "text": "Your document text here...",
  "metadata": { "source": "my_doc.pdf" }
}
```

**Response:**
```json
{
  "message": "Document ingested successfully",
  "chunks_stored": 4
}
```

---

### `POST /api/v1/query/`

Embeds a question, retrieves top-k similar chunks, and generates an answer.

**Request:**
```json
{
  "question": "What is FastAPI?",
  "top_k": 5
}
```

**Response:**
```json
{
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern web framework...",
  "sources": [
    {
      "text": "FastAPI is a modern, fast...",
      "score": 0.91,
      "metadata": { "source": "my_doc.pdf" }
    }
  ]
}
```

---

### `GET /health`

Returns `{ "status": "ok" }`.

## Configuration

All settings are controlled via `.env`:

| Variable | Default | Description |
|---|---|---|
| `NUGEN_API_KEY` | — | **Required.** Your Nugen API key |
| `NUGEN_BASE_URL` | `https://api.nugen.in/inference` | Nugen API base URL |
| `NUGEN_EMBED_MODEL` | `nugen-flash-embed` | Embedding model |
| `NUGEN_CHAT_MODEL` | `nugen-flash-instruct` | Chat/completion model |
| `QDRANT_COLLECTION` | `rag_documents` | Qdrant collection name |
| `VECTOR_SIZE` | `768` | Embedding dimension |
| `TOP_K` | `5` | Number of chunks to retrieve |
| `SIMILARITY_THRESHOLD` | `0.7` | Minimum cosine score to include a chunk |
| `CHUNK_SIZE` | `512` | Words per chunk |
| `CHUNK_OVERLAP` | `64` | Overlap between consecutive chunks |

## RAG Pipeline Flow

```
Document text
     │
     ▼
[Chunker] — sliding window (CHUNK_SIZE / CHUNK_OVERLAP)
     │
     ▼
[Nugen Embed] — vector per chunk
     │
     ▼
[Qdrant :memory:] — upsert with cosine distance
     │
     ▼  (at query time)
[Nugen Embed] — embed the question
     │
     ▼
[Qdrant Search] — top-k cosine similarity
     │
     ▼
[Threshold Filter] — drop chunks below SIMILARITY_THRESHOLD
     │
     ▼
[Nugen Chat] — generate answer from context
     │
     ▼
Response with answer + sources
```

## Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

## Notes

- Qdrant runs fully **in-memory** — data is lost on server restart. To persist, swap `QdrantClient(":memory:")` for `QdrantClient(host="localhost", port=6333)`.
- The Nugen client uses `httpx.AsyncClient` for non-blocking I/O, keeping FastAPI fully async.
