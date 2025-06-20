# No config import needed for wikipedia_summary.py
import wikipedia

async def run(query: str) -> str:
    """Get a summary for a topic from Wikipedia."""
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return f"Error: {e}" 