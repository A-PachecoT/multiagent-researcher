import operator
from typing import Annotated, List, TypedDict, Optional

from langchain_core.messages import BaseMessage


class ResearchState(TypedDict):
    """Research state schema"""

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
    # Research stage tracking
    stage: Optional[str]
    # Research plan
    plan: Optional[str]
