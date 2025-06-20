# MCP Platform Monorepo

This repository contains two independent projects for building AI-powered tool platforms:

- **classic_api/**: FastAPI backend with a classic Streamlit client.
- **mcp_platform/**: Modern MCP server with an agent-powered Streamlit client.

See each subproject's README for details and setup instructions.

# 🤖 MCP (Multi-Component Platform)

A modern, extensible platform for building and deploying AI-powered tools with a beautiful Streamlit interface and FastMCP backend.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-00a393.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0+-FF4B4B.svg)](https://streamlit.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **🛠️ Modular Tool System**: Easily create and deploy new AI tools
- **🎯 FastAPI Backend**: High-performance, async-ready API endpoints
- **🤖 LangChain Integration**: Powerful agent-based interactions
- **🔍 Built-in Tools**: Ready-to-use tools for common tasks
- **📝 Detailed Documentation**: Comprehensive guides and examples
- **🔒 Secure Design**: Environment-based configuration management

## Quickstart

### classic_api (FastAPI + Streamlit)

1. **Start the backend (FastAPI server):**
   ```bash
   cd classic_api/backend
   pip install -r requirements.txt
   uvicorn app.fastapi_app:app --reload
   ```
2. **Start the frontend (Streamlit client):**
   ```bash
   cd ../../frontend
   pip install -r requirements.txt
   cp .env.example .env  # Set your OpenAI key and model
   streamlit run streamlit_app.py
   ```
3. **Open your browser:**
   - Visit [http://localhost:8501](http://localhost:8501) for the UI.
   - The FastAPI server runs at [http://localhost:8000](http://localhost:8000) by default.

---

### mcp_platform (MCP Server + Streamlit Agent Client)

1. **Start the backend (MCP server):**
   ```bash
   cd mcp_platform/backend
   pip install -r requirements.txt
   python -m app.mcp_server_app
   ```
2. **Start the frontend (Streamlit client):**
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   cp .env.example .env  # Set your OpenAI key and model
   streamlit run streamlit_app.py
   ```
3. **Open your browser:**
   - Visit [http://localhost:8501](http://localhost:8501) for the chat UI.
   - The MCP server runs at [http://localhost:8000/mcp](http://localhost:8000/mcp) by default.

---


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

