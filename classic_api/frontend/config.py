import os
from dotenv import load_dotenv
import requests

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    # Add more LLM endpoints or settings as needed

config = Config()


#def make_request(self):
#    response = requests.post("http://localhost:8000/tools/add", json={"a": 2, "b": 3})
#    print("RESPONSE TEXT:", response.text)
#    if not response.ok:
#        print("HTTP ERROR:", response.status_code, response.text)
#    return response.json().get("answer", "No answer returned.") 