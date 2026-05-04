from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_background: Optional[str]
    next: Optional[str]
    sql_result: Optional[str]
    rag_result: Optional[str]
    agent_used: Optional[str]
    cv_uploaded: Optional[bool]
    cv_file_path: Optional[str]