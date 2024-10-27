import logging
from typing import Dict, Optional

from agents.supervisor import create_workflow
from state import ResearchState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_research(topic: str) -> ResearchState:
    """Initialize the research state with a given topic"""
    return ResearchState(
        messages=[],
        team_members=["supervisor", "searcher", "scraper", "synthesizer", "writer"],
        next="supervisor",
        research_data={"topic": topic},
        content="",
    )


def run_research(topic: str) -> dict:
    """Run research workflow for a given topic"""
    try:
        # Initialize state
        initial_state = initialize_research(topic)

        # Create and compile workflow
        workflow = create_workflow()

        # Use invoke() instead of run()
        result = workflow.invoke(initial_state)

        return result
    except Exception as e:
        logging.error(f"Error during research: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    topic = "The impact of artificial intelligence on modern healthcare"
    result = run_research(topic)

    if result:
        print(f"Research completed. Content length: {len(result['content'])}")
        print(f"Sources used: {result['metadata'].get('sources_used', 0)}")
    else:
        print("Research failed. Check logs for details.")
