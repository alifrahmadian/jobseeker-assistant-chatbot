from app.utils import logger

import pandas as pd
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(ROOT_DIR, "data", "raw", "Resume.csv")
PROCESSED_PATH = os.path.join(ROOT_DIR, "data", "processed", "Resume_cleaned.csv")

def preprocess():
    df_raw = pd.read_csv(RAW_PATH)
    
    try:
        logger.info("Cleaning Resume data...")
        
        df_raw = df_raw.drop('Resume_html', axis=1)
        df_raw['Resume_str'] = df_raw['Resume_str'].str.strip()
        df_raw['Resume_str'] = df_raw['Resume_str'].str.replace(r'\n+', '\n', regex=True)
        
        logger.info("Data cleaned successfully")
    except Exception as e:
        logger.error(f"Error while cleaning data: {e}")
        raise
    
    try:
        logger.info("Saving the cleaned data...")
        
        df_raw.to_csv(PROCESSED_PATH, index=False)
        
        logger.info(f"Cleaned data saved to {PROCESSED_PATH}")
    except Exception as e:
        logger.error(f"Error saving the cleaned data: {e}")
        raise