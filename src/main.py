import logging
from typing import Dict, Optional

from agents.supervisor import create_workflow
from state import ResearchState
from settings import settings

# Use settings for logging configuration
logging.basicConfig(level=settings.log_level)
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


def run_research(topic: str) -> Optional[Dict]:
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
        logger.error(f"Error during research: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    topic = "The impact of artificial intelligence on modern healthcare"
    result = run_research(topic)

    if result:
        logger.info(f"Research completed. Content length: {len(result['content'])}")
        logger.info(f"Sources used: {result['metadata'].get('sources_used', 0)}")
    else:
        logger.error("Research failed. Check logs for details.")
