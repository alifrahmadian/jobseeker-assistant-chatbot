from app.utils import(
    QDRANT_API_KEY,
    QDRANT_URL,
    QDRANT_COLLECTION_NAME,
    load_embedder,
    logger
)

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

from langchain_qdrant import QdrantVectorStore


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)
    
def create_collection():
    try:
        if not client.collection_exists(QDRANT_COLLECTION_NAME):
            logger.info("Creating qdrant collection...")
            client.create_collection(
                    collection_name = QDRANT_COLLECTION_NAME,
                    vectors_config = VectorParams(size=1536, distance = Distance.COSINE)
                )
        else:
            logger.info("Collection already exist, skipping...")
    except Exception as e:
        logger.error(f"Error while creating qdrant collection: {e}")
        raise

embedder = load_embedder()

def get_vector_store():
    return QdrantVectorStore(
        client=client,
        collection_name=QDRANT_COLLECTION_NAME,
        embedding=embedder
    )

def insert_documents(documents):
    try:
        logger.info("Inserting documents to qdrant database...")
        vector_store = get_vector_store()
        vector_store.add_documents(documents)
        logger.info("Documents sucessfully inserted!")
    except Exception as e:
        logger.error(f"Error while inserting documents: {e}")
        raise