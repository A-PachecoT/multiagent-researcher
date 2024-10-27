"""Test utilities and mock classes"""
from unittest.mock import MagicMock, patch
from tests.fixtures import MOCK_OPENAI_RESPONSES, MOCK_SEARCH_RESULTS
import pytest


class MockOpenAI:  # Add this class back
    """Mock OpenAI API with different response types"""
    def __init__(self, response_type: str = "content"):
        self.response_type = response_type
        self.invoke = MockResponse(response_type)


class MockResponse:
    """Mock response object for different types of responses"""
    def __init__(self, response_type: str = "content"):
        self.response_type = response_type
        self.content = MOCK_OPENAI_RESPONSES[response_type]

    def __call__(self, messages, *args, **kwargs):
        # Determine response type based on the message content
        if "synthesizer" in str(messages).lower():
            content = MOCK_OPENAI_RESPONSES["synthesis"]
        elif "writer" in str(messages).lower():
            content = MOCK_OPENAI_RESPONSES["content"]
        else:
            content = MOCK_OPENAI_RESPONSES[self.response_type]
        return MagicMock(content=content)


class MockDuckDuckGo:
    """Mock DuckDuckGo search with predefined results"""
    def invoke(self, query):
        return MOCK_SEARCH_RESULTS.copy()  # Return a copy to prevent modifications


@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses"""
    with patch('langchain_openai.ChatOpenAI') as mock:
        mock.return_value.invoke = MockResponse()
        yield mock