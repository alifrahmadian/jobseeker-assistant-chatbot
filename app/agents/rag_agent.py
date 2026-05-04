from app.graphs import State
from app.utils import logger, load_llm, langfuse_handler
from app.prompts import rag_prompt
from app.tools import rag_tool

from langchain_core.messages import AIMessage

llm = load_llm()
chain = rag_prompt | llm

def rag_agent(state: State) -> dict:
    try:
        logger.info("RAG agent started...")
        last_message = state["messages"][-1].content
        logger.debug(f"User message: {last_message}")
        
        logger.info("Invoking RAG tool to retrieve context...")
        rag_context = rag_tool.invoke(last_message)
        logger.debug(f"RAG context retrieved: {rag_context[:100]}...")
        
        logger.info("Generating response...")
        response = chain.invoke(
            {
                "user_message": last_message,
                "context": rag_context
            },
            config={"callbacks": [langfuse_handler]}
        )
        
        logger.info("RAG agent completed succesfully!")
        return {
            "messages": [AIMessage(content=response.content)],
            "rag_result": rag_context,
            "agent_used": "rag_agent"
        }
    except Exception as e:
        logger.error(f"RAG agent error: {e}")
        return {
            "messages": [AIMessage(content="Sorry, I encountered an error while processing your request.")],
            "agent_used": "rag_agent"
        }