from src.state import ResearchState
from src.agents.supervisor import create_workflow

def initialize_research(topic: str) -> ResearchState:
    """Initialize the research state with a given topic"""
    return ResearchState(
        messages=[],
        team_members=["supervisor", "searcher", "scraper", "synthesizer", "writer"],
        next="supervisor",
        research_data={},
        content=""
    )

def run_research(topic: str):
    """Main entry point for running research workflow"""
    workflow = create_workflow()
    initial_state = initialize_research(topic)
    
    # Run the workflow
    final_state = workflow.run(initial_state)
    return final_state["content"]
