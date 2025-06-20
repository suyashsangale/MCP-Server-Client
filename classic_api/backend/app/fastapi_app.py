from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import asyncio

app = FastAPI()

# --- Tool Request Models ---
class GreetRequest(BaseModel):
    name: str
class AddRequest(BaseModel):
    a: int
    b: int
class ReverseStringRequest(BaseModel):
    s: str
class WordCountRequest(BaseModel):
    s: str
class WikipediaSummaryRequest(BaseModel):
    query: str
class WebSearchRequest(BaseModel):
    query: str
class PythonExecRequest(BaseModel):
    code: str
class ToolQuestionRequest(BaseModel):
    question: str

# --- Tool Imports ---
from tools.greet import run as greet
from tools.add import run as add
from tools.reverse_string import run as reverse_string
from tools.word_count import run as word_count
from tools.wikipedia_summary import run as wikipedia_summary
from tools.web_search import run as web_search
from tools.python_exec import run as python_exec
from tools.tool1 import run as tool1
from tools.tool2 import run as tool2

# --- Endpoints ---
@app.post("/tools/greet")
async def greet_endpoint(req: GreetRequest):
    return {"answer": await greet(req.name)}

@app.post("/tools/add")
async def add_endpoint(req: AddRequest):
    return {"answer": await add(req.a, req.b)}

@app.post("/tools/reverse_string")
async def reverse_string_endpoint(req: ReverseStringRequest):
    return {"answer": await reverse_string(req.s)}

@app.post("/tools/word_count")
async def word_count_endpoint(req: WordCountRequest):
    return {"answer": await word_count(req.s)}

@app.post("/tools/wikipedia_summary")
async def wikipedia_summary_endpoint(req: WikipediaSummaryRequest):
    return {"answer": await wikipedia_summary(req.query)}

@app.post("/tools/web_search")
async def web_search_endpoint(req: WebSearchRequest):
    return {"answer": await web_search(req.query)}

@app.post("/tools/python_exec")
async def python_exec_endpoint(req: PythonExecRequest):
    return {"answer": await python_exec(req.code)}

@app.post("/tools/tool1")
async def tool1_endpoint(req: ToolQuestionRequest):
    # tool1 is sync, so run in threadpool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, tool1, req.dict())
    return result

@app.post("/tools/tool2")
async def tool2_endpoint(req: ToolQuestionRequest):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, tool2, req.dict())
    return result 