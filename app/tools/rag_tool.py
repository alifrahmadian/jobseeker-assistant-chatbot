from langchain_core.tools import tool
from app.utils import logger
from app.database import get_retriever

retriever = get_retriever()

@tool
def rag_tool(query: str) -> str:
    """
    Use this tool to search and retrieve relevant resume information based on semantic similarity. Use this for questions that require understanding context, finding similar profiles, or getting qualitative insights from resume content.
    
    Examples:
    1. 'Find resumes similar to a data scientist background'
    2. 'What kind of experience do people in healthcare category have?'
    3. 'Show me resumes with machine learning experience'
    """
    
    try:
        logger.info("Invoking RAG tool...")
        
        docs = retriever.invoke(query)
        result = "\n\n".join([doc.page_content for doc in docs])
        
        logger.info("RAG tool executed successfully!")
        return result
    except Exception as e:
        logger.error(f"Error in RAG tool: {e}")
        return f"Error retrieving information: {e}"
