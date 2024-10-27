from typing import Dict, List
from urllib.parse import urlparse
from settings import settings

import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class SearchAgent:
    def __init__(self, model: str = settings.gpt_model):
        self.llm = ChatOpenAI(
            model=model,
            temperature=settings.temperature,
            api_key=settings.openai_api_key
        )
        self.search_tool = DuckDuckGoSearchResults(num_results=3)  # Limit results
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a research agent. Generate relevant search queries "
                    "for the given topic and analyze search results.",
                ),
                (
                    "user",
                    "Research topic: {topic}\n" "Current findings: {current_findings}",
                ),
            ]
        )

    def search(self, topic: str, current_findings: Dict) -> List[Dict]:
        """Execute search and return relevant results"""
        try:
            results = self.search_tool.invoke(topic)
            return self._filter_results(results)
        except Exception as e:
            # Log error and return empty list instead of failing
            return []

    def _filter_results(self, results: List[Dict]) -> List[Dict]:
        """Filter and validate search results"""
        return [
            result for result in results if self._is_valid_url(result.get("link", ""))
        ]

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


class ScraperAgent:
    def __init__(self, model: str = settings.gpt_model):
        self.llm = ChatOpenAI(
            model=model,
            temperature=settings.temperature,
            api_key=settings.openai_api_key
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a content scraper. Extract and summarize relevant "
                    "information from the provided content.",
                ),
                ("user", "Content: {content}\nContext: {context}"),
            ]
        )

    def scrape(self, url: str, context: Dict) -> Dict:
        """Scrape and process content from URL"""
        try:
            content = self._fetch_content(url)
            response = self.llm.invoke(
                self.prompt.format_messages(
                    content=content[:4000], context=str(context)  # Limit content length
                )
            )

            return {"url": url, "summary": response.content, "raw_content": content}
        except Exception as e:
            return {"url": url, "error": str(e)}

    def _fetch_content(self, url: str) -> str:
        """Fetch and clean content from URL"""
        response = requests.get(url, headers={"User-Agent": "Research Bot 1.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        return soup.get_text()


def research_team_step(state: Dict) -> Dict:
    """Coordinate research team activities"""
    search_agent = SearchAgent()
    scraper_agent = ScraperAgent()

    # Get topic from state
    topic = state.get("topic") or state.get("research_data", {}).get("topic")
    if not topic:
        raise ValueError("No topic found in state")

    # Execute search with error handling
    try:
        search_results = search_agent.search(topic, state.get("research_data", {}))
        
        # Scrape and process results
        scraped_data = []
        for result in search_results[:3]:  # Limit to top 3 results
            try:
                scraped = scraper_agent.scrape(result["link"], {"topic": topic})
                if "error" not in scraped:  # Only add successful scrapes
                    scraped_data.append(scraped)
            except Exception:
                continue  # Skip failed scrapes

        # Ensure we have at least some data
        if not scraped_data:
            scraped_data = [{"url": "example.com", "summary": "No valid results found"}]

        # Update state
        state["research_data"]["sources"] = scraped_data
        state["stage"] = "content"
        state["next"] = "content_team"
        
        return state
    except Exception as e:
        # Handle any remaining errors
        state["error"] = str(e)
        state["next"] = "FINISH"
        return state
