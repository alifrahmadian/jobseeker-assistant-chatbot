from app.graphs import State
from app.utils import logger, load_llm, langfuse_handler
from app.prompts import sql_agent_prompt
from app.tools import sql_tool

from langchain_core.messages import AIMessage

llm = load_llm()
chain = sql_agent_prompt | llm

def sql_agent(state: State) -> dict:
    try:
        logger.info("SQL agent started...")
        last_message = state["messages"][-1].content
        logger.debug(f"User message: {last_message}")
        
        logger.info("Invoking SQL tool to retrieve structured data...")
        sql_result = sql_tool.invoke(last_message)
        logger.debug(f"SQL result retrieved: {sql_result}")
        
        logger.info("Generating response...")
        response = chain.invoke(
            {
                "user_message": last_message,
                "sql_result": sql_result
            },
            config={"callbacks": [langfuse_handler]}
        )
        
        logger.info("SQL agent completed successfully!")
        return {
            "messages": [AIMessage(content=response.content)],
            "sql_result": sql_result,
            "agent_used": "sql_agent"
        }
    except Exception as e:
        logger.error(f"SQL agent error: {e}")
        return {
            "messages": [AIMessage(content="Sorry, I encountered an error while processing your request.")],
            "agent_used": "sql_agent"
        }