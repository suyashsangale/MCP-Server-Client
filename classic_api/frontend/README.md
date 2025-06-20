# Classic API Streamlit Client

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
streamlit run streamlit_app.py
```

- The client will run at http://localhost:8501 (default)
- Make sure the FastAPI server is running at http://localhost:8000

## Environment Variables

Copy `.env.example` to `.env` and set your OpenAI API key and model:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
``` 