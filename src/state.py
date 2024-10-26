from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

class ResearchState(TypedDict):
    # Messages between agents
    messages: Annotated[List[BaseMessage], operator.add]
    # Track team members
    team_members: List[str]
    # Current active agent
    next: str
    # Research data storage
    research_data: dict
    # Final output
    content: str
