from app.utils import(
    QDRANT_API_KEY,
    QDRANT_URL,
    QDRANT_COLLECTION_NAME,
    load_llm,
    load_embedder,
    logger
)

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

from langchain_qdrant import QdrantVectorStore

def get_qdrant_client():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )
    
    return client