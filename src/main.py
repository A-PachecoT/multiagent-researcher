import logging
from typing import Dict, Optional

from src.agents.supervisor import create_workflow
from src.state import ResearchState

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


def run_research(topic: str) -> Optional[Dict]:
    """Main entry point for running research workflow"""
    try:
        logger.info(f"Starting research on topic: {topic}")
        workflow = create_workflow()
        initial_state = initialize_research(topic)

        # Run the workflow
        final_state = workflow.run(initial_state)

        logger.info("Research completed successfully")
        return {
            "content": final_state["content"],
            "metadata": final_state.get("metadata", {}),
            "research_data": final_state["research_data"],
        }

    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
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
