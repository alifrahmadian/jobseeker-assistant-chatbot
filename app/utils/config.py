from langchain_openai import ChatOpenAI
from langfuse import get_client
from dotenv import load_dotenv

import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL")

def load_llm(temperature, model):
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        )
    
    return llm