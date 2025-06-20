import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

config = Config()

# Usage:
# from config import config
# api_key = config.OPENAI_API_KEY
# model = config.OPENAI_MODEL 