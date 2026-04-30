import pandas as pd
import os

from langchain_core.documents import Document
from app.utils import logger
from app.database import insert_documents

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_PATH = os.path.join(ROOT_DIR, "data", "processed", "Resume_cleaned.csv")

def embed_and_insert():
    try:
        logger.info("Starting embedding pipeline...")
        df_processed = pd.read_csv(PROCESSED_PATH)
        
        docs = [
            Document(
                id = row['ID'],
                page_content = row['Resume_str'],
                metadata = {
                    "resume_id": row['ID'],
                    "category": row['Category']
                }
            )
            for _, row in df_processed.iterrows()
        ]
        
        insert_documents(docs)
        logger.info("Embedding pipeline completed!")
    except Exception as e:
        logger.error(f"Error during embedding pipeline: {e}")
        raise