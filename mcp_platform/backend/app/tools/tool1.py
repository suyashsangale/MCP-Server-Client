# No config import needed for tool1.py

def run(input: dict):
    question = input.get("question", "")
    return {"answer": f"Tool1 received: {question}"} 