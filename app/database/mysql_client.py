from app.utils import (
    MYSQL_DB_HOST, 
    MYSQL_DB_USER, 
    MYSQL_DB_PASSWORD, 
    MYSQL_DB_DATABASE,
    logger
)
from app.database.queries import *

import mysql.connector

def get_connection():
    try:
        logger.debug(f"Connecting to MySQL at {MYSQL_DB_HOST} with user {MYSQL_DB_USER}")
        logger.debug(f"Using database: {MYSQL_DB_DATABASE}")
        connection = mysql.connector.connect(
            host=MYSQL_DB_HOST,
            user=MYSQL_DB_USER,
            password=MYSQL_DB_PASSWORD,
            database=MYSQL_DB_DATABASE
        )
        
        logger.info("Successfully connected to MySQL database.")
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to MySQL database: {err}")
        raise

def create_tables():
    logger.info("Creating tables...")
    connection = get_connection()
    cursor = connection.cursor()
    
    queries = [
        CREATE_RESUMES_TABLE,
        CREATE_SKILLS_TABLE,
        CREATE_EXPERIENCES_TABLE,
        CREATE_EDUCATIONS_TABLE
    ]
    
    try:
        for query in queries:
            cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        logger.error(f"MySQL error creating tables: {e}")
        raise
    
    cursor.close()
    connection.close()

def insert_resume(connection, id:str, category:str, job_title:str):
    cursor = connection.cursor()
    
    query = """
        INSERT INTO resumes(id, category, job_title)
        VALUES(%s, %s, %s);
    """
    
    try:
        values = (id, category, job_title)
        cursor.execute(query, values)
        logger.debug(f"Inserting resumes with ID {id}")
        logger.info("Resume successfully inserted!")
    except mysql.connector.Error as e:
        logger.error(f"Error inserting resumes: {e}")
        raise
    finally:
        cursor.close()

def insert_skills(connection, resume_id:str, skills:list):
    cursor = connection.cursor()
    
    query = """
        INSERT INTO skills(resume_id, skill)
        VALUES(%s, %s);
    """
    
    try:
        for skill in skills:
            values = (resume_id, skill)
            cursor.execute(query, values)
            logger.debug(f"Inserting skills from resume_id {resume_id}")
        logger.info(f"Skills successfully inserted for resume_id {resume_id}!")
    except mysql.connector.Error as e:
        logger.error(f"Error inserting skills: {e}")
        raise
    finally:
        cursor.close()

def insert_experiences(connection, resume_id:str, experiences:list):
    cursor = connection.cursor()
    
    query = """
        INSERT INTO experiences(resume_id, job_title, company_name, start_date, end_date, description)
        VALUES(%s, %s, %s, %s, %s, %s);
    """
    
    try:
        for experience in experiences:
            values = (
                resume_id,
                experience.job_title,
                experience.company_name,
                experience.start_date,
                experience.end_date,
                experience.description
            )
            cursor.execute(query, values)
            logger.debug(f"Inserting experience with resume_id {resume_id}")
        logger.info(f"Experiences successfully inserted for resume_id {resume_id}!")
    except mysql.connector.Error as e:
        logger.error(f"Error inserting experiences: {e}")
        raise
    finally:
        cursor.close()

def insert_educations(connection, resume_id:str, educations:list):
    cursor = connection.cursor()
    
    query = """
        INSERT INTO educations(resume_id, degree, institution, year) 
        VALUES(%s, %s, %s, %s);
    """
    
    try:
        for education in educations:
            values = (
                resume_id,
                education.degree,
                education.institution,
                education.year
            )
            cursor.execute(query, values)
            logger.debug(f"Inserting education with resume_id {resume_id}")
        logger.info(f"Educations successfully inserted for resume_id {resume_id}!")
    except mysql.connector.Error as e:
        logger.error(f"Error inserting educations: {e}")
        raise
    finally:
        cursor.close()

if __name__ == "__main__":
    connection = get_connection()
    if connection:
        print("Connection successful!")
        connection.close()