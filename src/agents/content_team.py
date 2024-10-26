from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class SynthesizerAgent:
    def __init__(self, model: str = "gpt-3.5-turbo-16k"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research synthesizer. Analyze and combine information "
                      "from multiple sources to create a coherent understanding. "
                      "Identify patterns, conflicts, and gaps in the research."),
            ("user", "Topic: {topic}\nSources:\n{sources}\n\n"
                    "Create a comprehensive synthesis of the research findings.")
        ])

    def synthesize(self, topic: str, sources: List[Dict]) -> Dict:
        """Synthesize information from multiple sources"""
        # Format sources for prompt
        sources_text = "\n".join(
            f"Source {i+1}: {source.get('summary', '')}"
            for i, source in enumerate(sources)
        )
        
        response = self.llm.invoke(
            self.prompt.format_messages(
                topic=topic,
                sources=sources_text
            )
        )
        
        return {
            "synthesis": response.content,
            "source_count": len(sources)
        }

class WriterAgent:
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research writer. Create well-structured, clear, "
                      "and engaging content based on the synthesized research. "
                      "Include proper citations and maintain academic rigor."),
            ("user", "Topic: {topic}\nSynthesis: {synthesis}\n\n"
                    "Create a comprehensive research article.")
        ])

    def write(self, topic: str, synthesis: Dict) -> Dict:
        """Create final research content"""
        response = self.llm.invoke(
            self.prompt.format_messages(
                topic=topic,
                synthesis=synthesis["synthesis"]
            )
        )
        
        return {
            "content": response.content,
            "metadata": {
                "sources_used": synthesis.get("source_count", 0)
            }
        }

def content_team_step(state: Dict) -> Dict:
    """Coordinate content team activities"""
    synthesizer = SynthesizerAgent()
    writer = WriterAgent()
    
    # Get sources from research data
    sources = state.get("research_data", {}).get("sources", [])
    
    # Synthesize research
    synthesis = synthesizer.synthesize(
        state["topic"],
        sources
    )
    state["research_data"]["synthesis"] = synthesis
    
    # Create final content
    final_content = writer.write(
        state["topic"],
        synthesis
    )
    
    # Update state
    state["content"] = final_content["content"]
    state["metadata"] = final_content["metadata"]
    state["stage"] = "complete"
    
    return state
