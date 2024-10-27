import pytest
from unittest.mock import patch, MagicMock

from tests.fixtures import MOCK_SEARCH_RESULTS, MOCK_HTML_CONTENT, MOCK_OPENAI_RESPONSES
from tests.utils import MockOpenAI, MockDuckDuckGo

from agents.content_team import SynthesizerAgent, WriterAgent
from agents.research_team import ScraperAgent, SearchAgent
from main import initialize_research, run_research


@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses"""
    with patch('langchain_openai.ChatOpenAI') as mock:
        mock.return_value.invoke.return_value = MagicMock(
            content=MOCK_OPENAI_RESPONSES["content"]
        )
        yield mock


@pytest.fixture
def mock_duckduckgo():
    """Mock DuckDuckGo search results"""
    with patch('agents.research_team.DuckDuckGoSearchResults') as mock:  # Fix the path
        mock.return_value.invoke.return_value = MOCK_SEARCH_RESULTS
        yield mock


@pytest.fixture
def mock_requests():
    """Mock HTTP requests"""
    with patch('requests.get') as mock:
        mock.return_value.text = MOCK_HTML_CONTENT
        yield mock


def test_initialize_research():
    """Test research state initialization"""
    topic = "Test Topic"
    state = initialize_research(topic)

    assert state["next"] == "supervisor"
    assert state["research_data"]["topic"] == topic
    assert len(state["team_members"]) == 5
    assert state["stage"] == "planning"
    assert state["plan"] is None


@pytest.mark.usefixtures("mock_duckduckgo")
def test_search_agent():
    """Test search agent functionality with mocked DuckDuckGo"""
    agent = SearchAgent()
    results = agent.search("Python programming basics", {"existing": "none"})

    assert isinstance(results, list)
    assert len(results) == len(MOCK_SEARCH_RESULTS)
    assert results[0]["link"] == MOCK_SEARCH_RESULTS[0]["link"]


@pytest.mark.usefixtures("mock_openai", "mock_requests")
def test_scraper_agent():
    """Test scraper agent functionality with mocked requests"""
    agent = ScraperAgent()
    result = agent.scrape("https://python.org", {"topic": "Python programming"})

    assert "url" in result
    assert "summary" in result
    assert result["url"] == "https://python.org"


@pytest.mark.usefixtures("mock_openai")
def test_synthesizer_agent():
    """Test synthesizer agent functionality with mocked OpenAI"""
    agent = SynthesizerAgent()
    sources = [
        {"summary": "Python is a programming language"},
        {"summary": "Python is widely used in data science"},
    ]

    result = agent.synthesize("Python programming", sources)

    assert "synthesis" in result
    assert result["source_count"] == 2
    assert result["synthesis"] == MOCK_OPENAI_RESPONSES["synthesis"]  # Updated assertion


@pytest.mark.usefixtures("mock_openai")
def test_writer_agent():
    """Test writer agent functionality with mocked OpenAI"""
    agent = WriterAgent()
    synthesis = {
        "synthesis": MOCK_OPENAI_RESPONSES["synthesis"],  # Use consistent test data
        "source_count": 2,
    }

    result = agent.write("Python programming", synthesis)

    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["sources_used"] == synthesis["source_count"]
    assert result["content"] == MOCK_OPENAI_RESPONSES["content"]


@pytest.mark.usefixtures("mock_openai", "mock_duckduckgo", "mock_requests")
def test_full_research_workflow():
    """Test the complete research workflow with all mocks"""
    topic = "Python programming basics"
    result = run_research(topic)
    
    # Add debug logging
    if result is None:
        print("Result is None. Check the state initialization.")
    
    assert result is not None
    assert "content" in result
    assert "metadata" in result
    assert "research_data" in result
    assert len(result["content"]) > 0


if __name__ == "__main__":
    pytest.main([__file__])
