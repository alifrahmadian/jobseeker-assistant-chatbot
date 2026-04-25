from app.utils import (
    MYSQL_DB_HOST, 
    MYSQL_DB_USER, 
    MYSQL_DB_PASSWORD, 
    MYSQL_DB_DATABASE,
    logger
)

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
    pass

def insert_resumes():
    pass

def insert_skills():
    pass

def insert_experiences():
    pass

def insert_educations():
    pass

if __name__ == "__main__":
    connection = get_connection()
    if connection:
        print("Connection successful!")
        connection.close()