from app.graphs import State
from app.utils import logger, load_llm, langfuse_handler
from app.prompts import CV_ANALYSIS_PROMPT
from app.tools import rag_tool, sql_tool, cv_parser_tool

from langchain.agents import create_agent
from langchain_core.messages import AIMessage

llm = load_llm()

def cv_analysis_agent(state: State) -> dict:
    try:
        logger.info("CV Analysis agent started...")
        
        user_background = state.get("user_background") or "No CV uploaded yet"
        system_prompt = f"{CV_ANALYSIS_PROMPT}\nUser Background: {user_background}"
        
        agent = create_agent(
            model=llm,
            tools=[rag_tool, sql_tool, cv_parser_tool],
            system_prompt=system_prompt,
        )
        
        response = agent.invoke(
            state,
            config={"callbacks": [langfuse_handler]}
        )
        
        logger.info("CV Analysis agent completed!")
        return {
            "messages": response["messages"],
            "agent_used": "cv_analysis_agent"
        }
    except Exception as e:
        logger.error(f"CV Analysis agent error: {e}")
        return {
            "messages": [AIMessage(content="Sorry, I encountered an error while analyzing your CV.")],
            "agent_used": "cv_analysis_agent"
        }