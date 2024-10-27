import pytest

from agents.content_team import SynthesizerAgent, WriterAgent
from agents.research_team import ScraperAgent, SearchAgent
from agents.supervisor import SupervisorAgent
from main import initialize_research, run_research


def test_initialize_research():
    """Test research state initialization"""
    topic = "Test Topic"
    state = initialize_research(topic)

    assert state["next"] == "supervisor"
    assert "topic" in state["research_data"]
    assert state["research_data"]["topic"] == topic
    assert len(state["team_members"]) == 5


def test_search_agent():
    """Test search agent functionality"""
    agent = SearchAgent()
    results = agent.search("Python programming basics", {"existing": "none"})

    assert isinstance(results, list)
    assert len(results) > 0
    assert "link" in results[0]


def test_scraper_agent():
    """Test scraper agent functionality"""
    agent = ScraperAgent()
    result = agent.scrape("https://python.org", {"topic": "Python programming"})

    assert "url" in result
    assert "summary" in result or "error" in result


def test_synthesizer_agent():
    """Test synthesizer agent functionality"""
    agent = SynthesizerAgent()
    sources = [
        {"summary": "Python is a programming language"},
        {"summary": "Python is widely used in data science"},
    ]

    result = agent.synthesize("Python programming", sources)

    assert "synthesis" in result
    assert "source_count" in result
    assert result["source_count"] == 2


def test_writer_agent():
    """Test writer agent functionality"""
    agent = WriterAgent()
    synthesis = {
        "synthesis": "Python is a versatile programming language used in data science",
        "source_count": 2,
    }

    result = agent.write("Python programming", synthesis)

    assert "content" in result
    assert "metadata" in result
    assert "sources_used" in result["metadata"]


def test_full_research_workflow():
    """Test the complete research workflow"""
    topic = "Python programming basics"
    result = run_research(topic)

    assert result is not None
    assert "content" in result
    assert "metadata" in result
    assert "research_data" in result
    assert len(result["content"]) > 0


if __name__ == "__main__":
    pytest.main([__file__])
