# MCP Platform Monorepo

This repository contains two independent projects for building AI-powered tool platforms:

- **classic_api/**: FastAPI backend with a classic Streamlit client.
- **mcp_platform/**: Modern MCP server with an agent-powered Streamlit client.

See each subproject's README for details and setup instructions.

# 🤖 MCP (Multi-Component Platform)

A modern, extensible platform for building and deploying AI-powered tools with a beautiful Streamlit interface and FastAPI backend.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-00a393.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0+-FF4B4B.svg)](https://streamlit.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **🛠️ Modular Tool System**: Easily create and deploy new AI tools
- **🎯 FastAPI Backend**: High-performance, async-ready API endpoints
- **💻 Beautiful Streamlit UI**: Modern, responsive chat interface
- **🤖 LangChain Integration**: Powerful agent-based interactions
- **🔍 Built-in Tools**: Ready-to-use tools for common tasks
- **📝 Detailed Documentation**: Comprehensive guides and examples
- **🔒 Secure Design**: Environment-based configuration management

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp.git
cd mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the FastAPI server (in one terminal)
cd server
uvicorn app.fastapi_app:app --reload --host 0.0.0.0 --port 8000

# Start the Streamlit client (in another terminal)
cd ../client
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` to interact with the chat interface!

## 📚 Documentation

### Project Structure
```
mcp/
├── server/
│   ├── app/
│   │   ├── tools/          # Tool implementations
│   │   ├── config.py       # Server configuration
│   │   └── fastapi_app.py  # FastAPI application
│   └── requirements.txt
├── client/
│   ├── streamlit_app.py    # Streamlit interface
│   ├── config.py           # Client configuration
│   └── requirements.txt
└── docs/
    ├── tools/              # Tool documentation
    ├── development.md      # Development guide
    └── deployment.md       # Deployment guide
```

### MCP Protocol Implementation

The MCP (Multi-Component Platform) protocol is implemented using FastAPI and Streamlit, providing a robust and flexible communication layer between components:

#### Server-Side Implementation
1. **FastAPI Core**
   ```python
   from fastapi import FastAPI
   from pydantic import BaseModel
   
   app = FastAPI()
   
   class ToolRequest(BaseModel):
       param: str
   
   @app.post("/tools/your_tool")
   async def your_tool_endpoint(req: ToolRequest):
       return {"answer": await process_tool(req.param)}
   ```
   - High-performance async endpoints
   - Automatic OpenAPI documentation
   - Built-in request validation
   - Type-safe request/response handling

2. **Tool Implementation**
   ```python
   # server/app/tools/your_tool.py
   async def run(param: str) -> str:
       """Process the tool request."""
       return f"Processed: {param}"
   ```
   - Modular tool organization
   - Async support by default
   - Clear separation of concerns

#### Client-Side Integration
1. **HTTP Client Wrappers**
   ```python
   async def tool_wrapper(param: str) -> str:
       async with httpx.AsyncClient() as client:
           response = await client.post(
               "http://localhost:8000/tools/your_tool",
               json={"param": param}
           )
           return response.json().get("answer")
   ```
   - Async HTTP communication
   - Clean error handling
   - Structured response parsing

2. **LangChain Tool Integration**
   ```python
   Tool(
       name="YourTool",
       func=tool_wrapper,
       description="Tool description"
   )
   ```
   - Seamless LangChain integration
   - Agent-based tool execution
   - Rich tool descriptions

#### Protocol Features
- **RESTful Design**: Clean, standard HTTP endpoints
- **Async Operations**: High-performance async communication
- **Type Safety**: Pydantic model validation
- **OpenAPI Support**: Auto-generated API documentation
- **Error Handling**: Standardized error responses
- **Logging**: Comprehensive request logging
- **Security**: Environment-based configuration
- **Scalability**: Easy to extend and modify

### Available Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| Add | Add two numbers | "Add 5 and 7" |
| ReverseString | Reverse a string | "Reverse hello world" |
| WordCount | Count words in text | "Count words in this sentence" |
| WikipediaSummary | Get Wikipedia summary | "Summarize Python programming" |
| WebSearch | Search the web | "Search latest AI news" |
| PythonExec | Execute Python code | "Calculate sum([1,2,3])" |
| Greet | Greet a person | "Greet Alice" |

## 🛠️ Creating New Tools

1. Create a new file in `server/app/tools/`:
```python
async def run(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"
```

2. Register in `server/app/fastapi_app.py`:
```python
@app.post("/tools/your_tool")
async def your_tool_endpoint(req: YourToolRequest):
    return {"answer": await your_tool(req.param)}
```

3. Add to Streamlit client in `client/streamlit_app.py`:
```python
Tool(
    name="YourTool",
    func=your_tool_wrapper,
    description="Your tool description"
)
```

See [Tool Development Guide](docs/development.md) for detailed instructions.

## 🔧 Configuration

### Required Environment Variables
```env
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
OPENAI_MODEL=gpt-3.5-turbo  # or your preferred model
```

### Optional Configuration
- `HOST`: FastAPI server host (default: 0.0.0.0)
- `PORT`: FastAPI server port (default: 8000)
- See [Configuration Guide](docs/configuration.md) for more options

## 🚀 Deployment

See [Deployment Guide](docs/deployment.md) for:
- Docker deployment
- Cloud hosting options
- Security considerations
- Scaling guidelines

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [OpenAI](https://openai.com/)
- [Tavily](https://tavily.com/)

## 📧 Contact

- Create an issue for bug reports or feature requests
- Pull requests are welcome!

---

Made with ❤️ by [Your Name/Organization] 