# 🛠️ Tool Development Guide

This guide explains how to create new tools for the MCP platform.

## Table of Contents
- [Tool Structure](#tool-structure)
- [Creating a New Tool](#creating-a-new-tool)
- [Tool Best Practices](#tool-best-practices)
- [Testing Your Tool](#testing-your-tool)
- [Examples](#examples)

## Tool Structure

Each tool in MCP consists of three parts:
1. **Tool Implementation** (`server/app/tools/`)
2. **FastAPI Endpoint** (`server/app/fastapi_app.py`)
3. **Streamlit Integration** (`client/streamlit_app.py`)

### Basic Tool Template

```python
# server/app/tools/your_tool.py
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

async def run(param1: str, param2: Optional[int] = None) -> Any:
    """
    Tool description - explain what your tool does.

    Args:
        param1: Description of param1
        param2: Description of param2 (optional)

    Returns:
        The result of the tool's operation

    Raises:
        ValueError: If parameters are invalid
    """
    try:
        # Your tool logic here
        result = f"Processed {param1} with {param2}"
        logger.info(f"Tool executed successfully with params: {param1}, {param2}")
        return result
    except Exception as e:
        logger.error(f"Error in tool execution: {e}")
        return f"Error: {str(e)}"
```

## Creating a New Tool

1. **Create the Tool File**
   ```bash
   touch server/app/tools/your_tool.py
   ```

2. **Implement the Tool**
   ```python
   # server/app/tools/your_tool.py
   async def run(param: str) -> str:
       return f"Processed: {param}"
   ```

3. **Create FastAPI Endpoint**
   ```python
   # server/app/fastapi_app.py
   from pydantic import BaseModel
   
   class YourToolRequest(BaseModel):
       param: str
   
   @app.post("/tools/your_tool")
   async def your_tool_endpoint(req: YourToolRequest):
       return {"answer": await your_tool(req.param)}
   ```

4. **Add Streamlit Integration**
   ```python
   # client/streamlit_app.py
   def your_tool_wrapper(param: str) -> str:
       async def _tool():
           async with httpx.AsyncClient() as client:
               response = await client.post(
                   "http://localhost:8000/tools/your_tool",
                   json={"param": param}
               )
               return response.json().get("answer", "No answer returned.")
       return asyncio.run(_tool())

   # Add to tools list
   Tool(
       name="YourTool",
       func=your_tool_wrapper,
       description="Description of what your tool does"
   )
   ```

## Tool Best Practices

1. **Error Handling**
   - Always use try-except blocks
   - Log errors appropriately
   - Return user-friendly error messages

2. **Input Validation**
   - Use Pydantic models for request validation
   - Add type hints to all parameters
   - Validate inputs before processing

3. **Async Support**
   - Make tools async when possible
   - Use `asyncio.gather` for parallel operations
   - Handle timeouts appropriately

4. **Documentation**
   - Add detailed docstrings
   - Include usage examples
   - Document any external dependencies

5. **Security**
   - Never expose sensitive data
   - Validate and sanitize inputs
   - Use environment variables for secrets

## Testing Your Tool

1. **Unit Tests**
   ```python
   # tests/tools/test_your_tool.py
   import pytest
   from app.tools.your_tool import run
   
   @pytest.mark.asyncio
   async def test_your_tool():
       result = await run("test_param")
       assert "Processed: test_param" in result
   ```

2. **API Tests**
   ```python
   from fastapi.testclient import TestClient
   
   def test_your_tool_endpoint():
       response = client.post("/tools/your_tool", json={"param": "test"})
       assert response.status_code == 200
       assert "answer" in response.json()
   ```

## Examples

### 1. Simple Calculator Tool
```python
# server/app/tools/calculator.py
async def run(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: Math expression (e.g., "2 + 2")
        
    Returns:
        Result of the calculation
    """
    try:
        # Use ast.literal_eval for safe evaluation
        import ast
        result = ast.literal_eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: Invalid expression - {str(e)}"
```

### 2. API Integration Tool
```python
# server/app/tools/weather.py
import aiohttp

async def run(city: str) -> str:
    """
    Get weather for a city using OpenWeatherMap API.
    """
    API_KEY = os.getenv("WEATHER_API_KEY")
    async with aiohttp.ClientSession() as session:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        async with session.get(url, params=params) as response:
            data = await response.json()
            return f"Temperature in {city}: {data['main']['temp']}°C"
```

### 3. Data Processing Tool
```python
# server/app/tools/text_analyzer.py
from collections import Counter
import re

async def run(text: str) -> dict:
    """
    Analyze text and return statistics.
    """
    words = re.findall(r'\w+', text.lower())
    return {
        "word_count": len(words),
        "unique_words": len(set(words)),
        "most_common": Counter(words).most_common(3)
    }
```

## Need Help?

- Check existing tools for examples
- Read the [API Documentation](api.md)
- Open an issue for questions
- Join our [Discord community](https://discord.gg/your-server)

---

Remember to update the [Available Tools](../README.md#available-tools) section in the main README when adding new tools! 