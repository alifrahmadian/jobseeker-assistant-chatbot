from langgraph.graph import StateGraph, END
from app.graphs import State
from app.agents import cv_analysis_agent, rag_agent, sql_agent, supervisor
from app.utils import logger

class JobseekerAssistantGraph(StateGraph):
    def __init__(self):
        super().__init__(State)
        
        # add nodes
        self.add_node("supervisor", supervisor)
        self.add_node("rag_agent", rag_agent)
        self.add_node("sql_agent", sql_agent)
        self.add_node("cv_analysis_agent", cv_analysis_agent)
        
        # entry point
        self.set_entry_point("supervisor")
        
        # conditional edges
        self.add_conditional_edges(
            "supervisor",
            self.route,
            {
                "rag_agent": "rag_agent",
                "sql_agent": "sql_agent",
                "cv_analysis_agent": "cv_analysis_agent"
            }
        )
        
        # edges to end
        self.add_edge("rag_agent", END)
        self.add_edge("sql_agent", END)
        self.add_edge("cv_analysis_agent", END)
        
    def route(self, state: State) -> str:
        return state["next"]

graph = JobseekerAssistantGraph().compile()
logger.info("Jobseeker Assistant Graph compiled successfully!")