from app.utils import logger, load_llm
from app.database import (
    get_connection,
    insert_resume,
    insert_skills,
    insert_experiences,
    insert_educations
)
from app.prompts import extraction_prompt
from app.schemas import Resume

import pandas as pd
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_PATH = os.path.join(ROOT_DIR, "data", "processed", "Resume_cleaned.csv")

llm = load_llm()
llm_with_structure = llm.with_structured_output(Resume)
chain = extraction_prompt | llm_with_structure

def extract_resume(resume_text: str) -> Resume:
    try:
        logger.info("Extracting resume...")
        result = chain.invoke(
            {"resume_text": resume_text}
        )
        logger.debug("Resume extracted successfully!")
        return result
    except Exception as e:
        logger.error(f"Error extracting resume: {e}")
        raise

def extract_and_insert():
    df_processed = pd.read_csv(PROCESSED_PATH)
    conn = get_connection()
    logger.info("Starting extraction pipeline...")
    
    try:
        for _, row in df_processed.iterrows():
            try:
                resume_id = row['ID']
                resume_text = row['Resume_str']
                category = row['Category']
                
                logger.info(f"Processing resume {resume_id}")
                
                result = extract_resume(resume_text)
                
                insert_resume(conn, resume_id, category, result.job_title)
                insert_skills(conn, resume_id, result.skills)
                insert_experiences(conn, resume_id, result.experiences)
                insert_educations(conn, resume_id, result.educations)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Error processing resume {resume_id}: {e}")
                continue
            
        logger.info("Extraction pipeline completed!")
    finally:
        conn.close()