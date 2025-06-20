# No config import needed for tool2.py

def run(input: dict):
    question = input.get("question", "")
    return {"answer": f"Tool2 processed: {question}"} 