# MCP Platform Project

## Overview
A modern, agent-based platform using the FastMCP protocol for tool orchestration, with a Streamlit client for chat and agent reasoning.

- **Backend:** MCP server (`backend/app/mcp_server_app.py`)
- **Frontend:** Streamlit MCP client (`frontend/streamlit_app.py`)

## Setup

### Backend
```bash
cd mcp_platform/backend
pip install -r requirements.txt
python app/mcp_server_app.py
```

### Frontend
```bash
cd mcp_platform/frontend
pip install -r requirements.txt
cp .env.example .env  # Set your OpenAI key and model
streamlit run streamlit_app.py
```

## Adding Tools
Add new tool modules to `backend/app/tools/` and register them in `mcp_server_app.py` using the `@mcp.tool` decorator.

## Usage
- Open the Streamlit UI and interact with the agent-powered chat interface. 