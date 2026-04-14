from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse import get_client
from dotenv import load_dotenv

import os

load_dotenv()

MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
MYSQL_DB_USER = os.getenv("MYSQL_DB_USER")
MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")
MYSQL_DB_DATABASE = os.getenv("MYSQL_DB_DATABASE")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL")

OPENAI_MODEL_NAME = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

def load_llm(temperature=0.1, model="gpt-4o-mini"):
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
    )
    
    return llm

def load_embedder(model="text-embedding-3-small"):
    embedding = OpenAIEmbeddings(
        model=model,
    )
    
    return embedding