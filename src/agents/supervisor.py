from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from agents.content_team import content_team_step
from agents.research_team import research_team_step
from state import ResearchState


class SupervisorAgent:
    def __init__(self, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model)
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
    return supervisor.create_research_plan(state)


def create_workflow() -> StateGraph:
    """Create the main research workflow graph"""
    workflow = StateGraph(ResearchState)  # Initialize with schema

    # Define state transitions
    def should_continue(state):
        return state["stage"] != "complete"

    # Add nodes and edges
    workflow.add_node("supervisor", supervisor_step)
    workflow.add_node("research_team", research_team_step)
    workflow.add_node("content_team", content_team_step)

    # Define workflow
    workflow.add_edge("supervisor", "research_team")
    workflow.add_edge("research_team", "content_team")
    workflow.add_conditional_edges(
        "content_team", should_continue, {True: "supervisor", False: END}
    )

    return workflow
