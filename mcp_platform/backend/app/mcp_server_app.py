import logging
import os
import asyncio
from fastmcp import FastMCP

# Import all tools
from tools.add import run as add
from tools.reverse_string import run as reverse_string
from tools.word_count import run as word_count
from tools.wikipedia_summary import run as wikipedia_summary
from tools.web_search import run as web_search
from tools.python_exec import run as python_exec
from tools.greet import run as greet
from tools.tool1 import run as tool1
from tools.tool2 import run as tool2

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("logs/mcp_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("MCP Demo Server 🚀")

# Register all tools using the @tool decorator pattern
@mcp.tool
async def add_tool(a: int, b: int) -> int:
    """Add two numbers."""
    return await add(a, b)

@mcp.tool
async def reverse_string_tool(s: str) -> str:
    """Reverse a string."""
    return await reverse_string(s)

@mcp.tool
async def word_count_tool(s: str) -> int:
    """Count words in text."""
    return await word_count(s)

@mcp.tool
async def wikipedia_tool(query: str) -> str:
    """Get Wikipedia summary."""
    return await wikipedia_summary(query)

@mcp.tool
async def web_search_tool(query: str) -> str:
    """Search the web."""
    return await web_search(query)

@mcp.tool
async def python_exec_tool(code: str) -> str:
    """Execute Python code."""
    return await python_exec(code)

@mcp.tool
async def greet_tool(name: str) -> str:
    """Greet someone."""
    return await greet(name)

@mcp.tool
async def tool1_tool(param: str) -> str:
    """Tool 1 implementation."""
    return await tool1(param)

@mcp.tool
async def tool2_tool(param: str) -> str:
    """Tool 2 implementation."""
    return await tool2(param)

if __name__ == "__main__":
    logger.info("Starting MCP server...")
    try:
        # Run with streamable-http transport on port 8000
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=8000,
            path="/mcp"  # Optional: specify the endpoint path
        )
    except Exception as e:
        logger.exception(f"MCP server failed to start: {e}") 