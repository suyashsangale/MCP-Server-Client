import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "YOUR_TAVILY_API_KEY")
    # Add more keys as needed

config = Config() 