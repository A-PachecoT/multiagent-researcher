from typing import Dict
from settings import settings

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from agents.content_team import content_team_step
from agents.research_team import research_team_step
from state import ResearchState


class SupervisorAgent:
    def __init__(self, model: str = settings.gpt_model):
        self.llm = ChatOpenAI(
            model=model,
            temperature=settings.temperature,
            api_key=settings.openai_api_key
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a research supervisor coordinating a team of agents. "
                    "Plan and delegate research tasks based on the given topic.",
                ),
                ("user", "Topic: {topic}\nCurrent research: {research_data}"),
            ]
        )

    def create_research_plan(self, state: Dict) -> Dict:
        """Create initial research plan and team assignments"""
        response = self.llm.invoke(
            self.prompt.format_messages(
                topic=state.get("topic", ""),
                research_data=str(state.get("research_data", {})),
            )
        )

        state["plan"] = response.content
        state["stage"] = "research"
        return state


def supervisor_step(state: Dict) -> Dict:
    """Supervisor step function for the workflow"""
    supervisor = SupervisorAgent()
    
    # Ensure topic is available in state
    topic = state.get("research_data", {}).get("topic", "")
    if not topic:
        raise ValueError("No topic provided in research data")
        
    updated_state = supervisor.create_research_plan(state)
    updated_state["next"] = "research_team"
    updated_state["topic"] = topic  # Ensure topic is in root state
    
    return updated_state


def create_workflow() -> StateGraph:
    """Create the main research workflow graph"""
    # Initialize with schema
    workflow = StateGraph(ResearchState)

    # Define state transitions
    def should_continue(state):
        return state["next"] != "FINISH"

    # Add nodes and edges
    workflow.add_node("supervisor", supervisor_step)
    workflow.add_node("research_team", research_team_step)
    workflow.add_node("content_team", content_team_step)

    # Define workflow
    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", "research_team")
    workflow.add_edge("research_team", "content_team")
    workflow.add_conditional_edges(
        "content_team", should_continue, {True: "supervisor", False: END}
    )

    # Compile the graph before returning
    return workflow.compile()
