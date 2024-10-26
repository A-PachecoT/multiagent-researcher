import logging
from src.main import run_research

logging.basicConfig(level=logging.INFO)

def run_example():
    """Run an example research task"""
    topics = [
        "The benefits of meditation for stress management",
        "Renewable energy technologies in 2024",
        "The impact of social media on mental health"
    ]
    
    for topic in topics:
        print(f"\n{'='*50}")
        print(f"Researching: {topic}")
        print(f"{'='*50}\n")
        
        result = run_research(topic)
        
        if result:
            print(f"\nResearch Summary:")
            print(f"- Content length: {len(result['content'])} characters")
            print(f"- Sources used: {result['metadata'].get('sources_used', 0)}")
            print("\nFirst 500 characters of content:")
            print(f"{result['content'][:500]}...")
        else:
            print("Research failed!")
        
        print(f"\n{'='*50}\n")

if __name__ == "__main__":
    run_example()
