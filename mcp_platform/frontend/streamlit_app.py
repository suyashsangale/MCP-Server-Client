import streamlit as st
import asyncio
import os
from fastmcp import Client
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from pydantic import SecretStr
from dotenv import load_dotenv
from config import config

load_dotenv()

st.set_page_config(page_title="🤖 MCP Chat (FastMCP)", page_icon="🤖", layout="wide")

MCP_SERVER_URL = st.sidebar.text_input("MCP Server URL", "http://localhost:8000/mcp")

# --- Tool Wrappers ---
def _extract_text(result):
    if result and hasattr(result[0], 'text'):
        return result[0].text
    return str(result[0]) if result else str(result)

def add_tool(input_str: str) -> str:
    async def run():
        a, b = map(int, input_str.strip().split())
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("add_tool", {"a": a, "b": b})
            return _extract_text(result)
    return asyncio.run(run())

def reverse_string_tool(text: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("reverse_string_tool", {"s": text})
            return _extract_text(result)
    return asyncio.run(run())

def word_count_tool(text: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("word_count_tool", {"s": text})
            return _extract_text(result)
    return asyncio.run(run())

def wikipedia_summary_tool(query: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("wikipedia_tool", {"query": query})
            return _extract_text(result)
    return asyncio.run(run())

def web_search_tool(query: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("web_search_tool", {"query": query})
            return _extract_text(result)
    return asyncio.run(run())

def python_exec_tool(code: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("python_exec_tool", {"code": code})
            return _extract_text(result)
    return asyncio.run(run())

def greet_tool(name: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("greet_tool", {"name": name})
            return _extract_text(result)
    return asyncio.run(run())

def tool1_tool(question: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("tool1_tool", {"question": question})
            return _extract_text(result)
    return asyncio.run(run())

def tool2_tool(question: str) -> str:
    async def run():
        async with Client(MCP_SERVER_URL) as client:
            result = await client.call_tool("tool2_tool", {"question": question})
            return _extract_text(result)
    return asyncio.run(run())

# --- LangChain Tools ---
tools = [
    Tool(name="Add", func=add_tool, description="Add two numbers. Input: '10 20'"),
    Tool(name="ReverseString", func=reverse_string_tool, description="Reverse a string. Input: the string to reverse."),
    Tool(name="WordCount", func=word_count_tool, description="Count the number of words in a string. Input: the string."),
    Tool(name="WikipediaSummary", func=wikipedia_summary_tool, description="Get a summary for a topic from Wikipedia. Input: the topic."),
    Tool(name="WebSearch", func=web_search_tool, description="Search the web for up-to-date information. Input: the search query."),
    Tool(name="PythonExec", func=python_exec_tool, description="Execute a Python code snippet and return the output. Input: a valid Python expression."),
    Tool(name="Greet", func=greet_tool, description="Greet a person by name. Input: the name."),
    Tool(name="Tool1", func=tool1_tool, description="Tool1: Input should be a question."),
    Tool(name="Tool2", func=tool2_tool, description="Tool2: Input should be a question."),
]

def get_llm():
    return ChatOpenAI(temperature=0, model=config.OPENAI_MODEL, api_key=SecretStr(config.OPENAI_API_KEY))

def get_agent():
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = get_llm()
    return initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=st.session_state.memory,
        return_intermediate_steps=True,
        max_iterations=15,
        max_execution_time=120,
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "latest_answer" not in st.session_state:
    st.session_state.latest_answer = None
if "latest_agent" not in st.session_state:
    st.session_state.latest_agent = None

# --- UI ---
st.title("🤖 MCP Chat (FastMCP Protocol)")

with st.sidebar:
    st.markdown("### 🛠️ Available Tools")
    for tool in tools:
        st.write(f"**{tool.name}**: {tool.description}")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.latest_answer = None
        st.session_state.latest_agent = None
        if "memory" in st.session_state:
            del st.session_state.memory
        st.rerun()

for msg in st.session_state.chat_history:
    st.markdown(f"**{msg['role'].title()}:** {msg['content']}")

question = st.text_input("Ask me anything:", key="input")
if st.button("Send") and question.strip():
    agent = get_agent()
    with st.spinner("Thinking..."):
        try:
            result = agent.invoke({"input": question})
            answer = result["output"] if isinstance(result, dict) and "output" in result else result
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append({"role": "agent", "content": answer})
            st.session_state.latest_answer = answer
            st.session_state.latest_agent = agent
            # Extract reasoning steps if available
            if isinstance(result, dict) and "intermediate_steps" in result:
                st.session_state.latest_steps = result["intermediate_steps"]
            else:
                st.session_state.latest_steps = None
        except Exception as e:
            st.session_state.latest_answer = f"Error: {e}"
            st.session_state.latest_agent = None
            st.session_state.latest_steps = None

# Show the AgentExecutor and answer below the send button
if st.session_state.latest_agent is not None:
    st.markdown("**AgentExecutor:**")
    st.write(st.session_state.latest_agent)
if st.session_state.latest_answer is not None:
    st.markdown("**Answer:**")
    st.success(st.session_state.latest_answer)
# Show reasoning steps if available
if "latest_steps" in st.session_state and st.session_state.latest_steps:
    st.markdown("**Agent Reasoning Steps:**")
    for i, step in enumerate(st.session_state.latest_steps):
        action, observation = step
        st.markdown(f"**Step {i+1}:**")
        st.markdown(f"- **Action:** {getattr(action, 'tool', str(action))}")
        st.markdown(f"- **Input:** {getattr(action, 'tool_input', str(action))}")
        st.markdown(f"- **Observation:** {observation}")

st.info("Set your OpenAI API key in the code or via environment variable for agent reasoning.") 