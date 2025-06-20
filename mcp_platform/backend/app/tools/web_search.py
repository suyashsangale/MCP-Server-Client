import logging
from tavily import TavilyClient
from tools.config import config  # Requires running as a module

logger = logging.getLogger(__name__)

tavily = TavilyClient(api_key=config.TAVILY_API_KEY)

async def run(query: str) -> str:
    """Search the web for up-to-date information."""
    try:
        logger.info(f"Web search query: {query}")
        result = tavily.search(query, max_results=3)
        logger.info(f"Web search result: {result}")
        return "\n\n".join([item['content'] for item in result['results']])
    except Exception as e:
        logger.error(f"Error in web_search for query '{query}': {e}")
        return f"Error: {e}" 