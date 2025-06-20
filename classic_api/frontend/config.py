import os
from dotenv import load_dotenv
import requests

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    # Add more LLM endpoints or settings as needed

config = Config()


#def make_request(self):
#    response = requests.post("http://localhost:8000/tools/add", json={"a": 2, "b": 3})
#    print("RESPONSE TEXT:", response.text)
#    if not response.ok:
#        print("HTTP ERROR:", response.status_code, response.text)
#    return response.json().get("answer", "No answer returned.") 