from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class SearchAgent:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model)
        self.search_tool = DuckDuckGoSearchResults()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research agent. Generate relevant search queries "
                      "for the given topic and analyze search results."),
            ("user", "Research topic: {topic}\nCurrent findings: {current_findings}")
        ])

    def search(self, topic: str, current_findings: Dict) -> List[Dict]:
        """Execute search and return relevant results"""
        response = self.llm.invoke(
            self.prompt.format_messages(
                topic=topic,
                current_findings=str(current_findings)
            )
        )
        
        # Execute search with multiple queries
        results = self.search_tool.invoke(topic)
        return self._filter_results(results)

    def _filter_results(self, results: List[Dict]) -> List[Dict]:
        """Filter and validate search results"""
        return [
            result for result in results
            if self._is_valid_url(result.get("link", ""))
        ]

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

class ScraperAgent:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a content scraper. Extract and summarize relevant "
                      "information from the provided content."),
            ("user", "Content: {content}\nContext: {context}")
        ])

    def scrape(self, url: str, context: Dict) -> Dict:
        """Scrape and process content from URL"""
        try:
            content = self._fetch_content(url)
            response = self.llm.invoke(
                self.prompt.format_messages(
                    content=content[:4000],  # Limit content length
                    context=str(context)
                )
            )
            
            return {
                "url": url,
                "summary": response.content,
                "raw_content": content
            }
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
    
    # Execute search
    search_results = search_agent.search(
        state["topic"],
        state.get("research_data", {})
    )
    
    # Scrape and process results
    scraped_data = []
    for result in search_results[:3]:  # Limit to top 3 results
        scraped = scraper_agent.scrape(
            result["link"],
            {"topic": state["topic"]}
        )
        scraped_data.append(scraped)
    
    # Update state
    state["research_data"]["sources"] = scraped_data
    state["stage"] = "content"
    
    return state
