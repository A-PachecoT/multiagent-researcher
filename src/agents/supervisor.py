from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

class SupervisorAgent:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research supervisor coordinating a team of agents. "
                      "Plan and delegate research tasks based on the given topic."),
            ("user", "Topic: {topic}\nCurrent research: {research_data}")
        ])

    def create_research_plan(self, state: Dict) -> Dict:
        """Create initial research plan and team assignments"""
        response = self.llm.invoke(
            self.prompt.format_messages(
                topic=state.get("topic", ""),
                research_data=str(state.get("research_data", {}))
            )
        )
        
        state["plan"] = response.content
        state["stage"] = "research"
        return state

def create_workflow() -> StateGraph:
    """Create the main research workflow graph"""
    workflow = StateGraph()
    
    # Define state transitions
    def should_continue(state):
        return state["stage"] != "complete"
    
    # Add nodes and edges
    workflow.add_node("supervisor", SupervisorAgent().create_research_plan)
    workflow.add_node("research_team", research_team_step)  # To be implemented
    workflow.add_node("content_team", content_team_step)    # To be implemented
    
    # Define workflow
    workflow.add_edge("supervisor", "research_team")
    workflow.add_edge("research_team", "content_team")
    workflow.add_conditional_edges(
        "content_team",
        should_continue,
        {
            True: "supervisor",
            False: END
        }
    )
    
    return workflow
