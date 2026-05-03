from langchain_core.tools import tool
from app.utils import logger, load_llm
from app.database import get_connection
from app.prompts import sql_prompt

llm = load_llm()
chain = sql_prompt | llm

def generate_sql(user_message:str) -> str:
    try:
        logger.info("Generating SQL query...")
        
        response = chain.invoke({"user_message": user_message})
        sql_query = response.content
        
        logger.debug(f"Generated SQL query: {sql_query}")
        logger.info("SQL query generated successfully!")
        
        return sql_query
    except Exception as e:
        logger.error(f"Error generating SQL query: {e}")
        raise
       
def execute_sql(query:str) -> str:
    if query == "INVALID_QUERY":
        logger.warning("LLM could not generate a valid SQL query")
        return "I could not generate a valid SQL query based on your question. Please try again!"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        logger.info("Executing SQL query...")
        logger.debug(f"Executing query: {query}")
        
        cursor.execute(query)
        results = cursor.fetchall()
        result_str = "\n".join([str(row) for row in results])
        
        if not results:
            return "No results found"
        
        return result_str
    except Exception as e:
        logger.error(f"Error executing SQL query: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

@tool
def sql_tool(user_message: str) -> str:
    """
    Use this tool to query structured information about the resume data from MySQL database. Use this for questions about statistics, counts, aggregations, filtering by category, skills, or any structured data queries. 
    
    Example: 
    1. 'How many resumes are in Engineering category?'
    2. 'What are the most common skills?'
    """
    
    try:
        logger.info(f"SQL tool called with: {user_message}")
        
        sql_query = generate_sql(user_message)
        result = execute_sql(sql_query)
        
        logger.info("SQL tool completed successfully!")
        
        return result
    except Exception as e:
        logger.error(f"Error in sql_tool: {e}")
        return f"Error in executing query: {str(e)}"