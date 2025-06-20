# No config import needed for word_count.py

async def run(s: str) -> int:
    """Count the number of words in a string."""
    return len(s.split()) 