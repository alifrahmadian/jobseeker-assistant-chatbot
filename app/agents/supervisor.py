from app.graphs import State
from app.utils import logger, load_llm, langfuse_handler
from app.prompts import supervisor_prompt

llm = load_llm()
chain = supervisor_prompt | llm

def supervisor(state: State) -> dict:
    try:
        last_message = state["messages"][-1].content
        
        response = chain.invoke(
            {"user_message": last_message},
            config={"callbacks": [langfuse_handler]}
        )
        next_agent = response.content.strip()
        
        VALID_AGENTS = ["sql_agent", "rag_agent", "cv_analysis_agent"]
        if next_agent not in VALID_AGENTS:
            logger.warning(f"Invalid agent: {next_agent}, defaulting to rag_agent")
            next_agent = "rag_agent"
        
        logger.info(f"Supervisor routed to: {next_agent}")
        return {"next": next_agent}
    except Exception as e:
        logger.error(f"Error in supervisor agent: {e}")
        return {"next": "rag_agent"}