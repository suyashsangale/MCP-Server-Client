import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")
    # Add more keys as needed

config = Config() 