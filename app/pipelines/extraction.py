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

def extract_resume(resume_text: str) -> Resume:
    pass

def extract_and_insert():
    pass