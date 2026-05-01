from app.database import create_tables, create_collection, get_connection
from app.pipelines import embed_and_insert, extract_and_insert, preprocess
from app.utils import logger

from langchain_community.callbacks import get_openai_callback

# def is_pipeline_done():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SHOW TABLES LIKE 'resumes'")
#     table_exists = cursor.fetchone()
    
#     if not table_exists:
#         cursor.close()
#         conn.close()
#         return False
    
#     cursor.execute("SELECT COUNT(*) FROM resumes")
#     count = cursor.fetchone()[0]
#     cursor.close()
#     conn.close()
#     return count > 0

def run_pipeline():
    # if is_pipeline_done():
    #     logger.info("Pipeline already done, skipping...")
    #     return
    
    create_tables()
    create_collection()
    preprocess()
    
    with get_openai_callback() as cb:
        embed_and_insert()      
        extract_and_insert()
            
        logger.info(f"Total tokens used: {cb.total_tokens}")
        logger.info(f"Prompt tokens: {cb.prompt_tokens}")
        logger.info(f"Completion tokens: {cb.completion_tokens}")
        logger.info(f"Total cost: ${cb.total_cost}")

if __name__ == "__main__":
    run_pipeline()