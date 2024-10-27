"""Test utilities and mock classes"""
from unittest.mock import MagicMock
from .fixtures import MOCK_OPENAI_RESPONSES, MOCK_SEARCH_RESULTS


class MockResponse:
    """Mock response object for different types of responses"""
    def __init__(self, content_type: str):
        self.content = MOCK_OPENAI_RESPONSES[content_type]

    def __call__(self, *args, **kwargs):
        return MagicMock(content=self.content)


class MockOpenAI:
    """Mock OpenAI API with different response types"""
    def __init__(self, response_type: str = "content"):
        self.response_type = response_type
        self.invoke = MockResponse(response_type)


class MockDuckDuckGo:
    """Mock DuckDuckGo search with predefined results"""
    def invoke(self, query):
        return MOCK_SEARCH_RESULTS
