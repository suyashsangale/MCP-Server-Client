# Classic API Project

## Overview
A traditional REST API platform using FastAPI for the backend and Streamlit for the client UI.

- **Backend:** FastAPI (`backend/app/fastapi_app.py`)
- **Frontend:** Streamlit (`frontend/streamlit_app.py`)

## Setup

### Backend
```bash
cd classic_api/backend
pip install -r requirements.txt
uvicorn app.fastapi_app:app --reload
```

### Frontend
```bash
cd classic_api/frontend
pip install -r requirements.txt
cp .env.example .env  # Set your OpenAI key and model
streamlit run streamlit_app.py
```

## Adding Tools
Add new tool modules to `backend/app/tools/` and register them in `fastapi_app.py`.

## Usage
- Open the Streamlit UI and interact with the tools via the REST API. 