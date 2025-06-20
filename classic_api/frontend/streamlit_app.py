import streamlit as st
import httpx
import asyncio
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import SystemMessagePromptTemplate
import datetime
import markdown
from config import config

# Set page configuration with a wider layout and custom theme
st.set_page_config(
    page_title="🤖 MCP Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# MCP Chat Agent\nA powerful agent with multiple tools."
    }
)

# Force light theme
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff;
        }
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }
        [data-testid="stToolbar"] {
            background-color: #ffffff;
        }
        .stMarkdown {
            color: #1f1f1f;
        }
        .stButton > button {
            background-color: #1f77b4;
            color: #ffffff;
        }
        .stTextInput > div > div > input {
            color: #1f1f1f;
            background-color: #ffffff;
        }
        
        /* Main container styling */
        .main {
            padding: 2rem;
            background-color: #ffffff;
        }
        
        /* Chat message styling */
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            position: relative;
            background-color: #ffffff;
            border: 1px solid #e1e4e8;
        }
        
        .user-message {
            background-color: #f0f2f6;
            color: #1f1f1f;
        }
        
        .agent-message {
            background-color: #e8f0fe;
            color: #1f1f1f;
        }
        
        /* Timestamp styling */
        .timestamp {
            font-size: 0.8rem;
            color: #666;
        }
        
        /* Agent reasoning box */
        .reasoning-box {
            background-color: #ffffff;
            border-left: 3px solid #1f77b4;
            padding: 1rem;
            margin: 0.5rem 0;
            color: #1f1f1f;
        }
        
        /* Tool execution box */
        .tool-box {
            background-color: #ffffff;
            border-left: 3px solid #ffc107;
            padding: 1rem;
            margin: 0.5rem 0;
            color: #1f1f1f;
        }
        
        /* Final answer box */
        .answer-box {
            background-color: #ffffff;
            border-left: 3px solid #28a745;
            padding: 1rem;
            margin: 0.5rem 0;
            color: #1f1f1f;
        }
        
        /* Header styling */
        .header {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            text-align: center;
            border: 1px solid #e1e4e8;
        }
        
        .header h1 {
            color: #1f1f1f;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: #666;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #ffffff;
            color: #1f1f1f;
        }
        
        /* Code blocks */
        code {
            color: #1f1f1f;
            background-color: #f6f8fa;
        }
        
        /* Links */
        a {
            color: #1f77b4;
        }
        
        /* Sidebar */
        [data-testid="stSidebarNav"] {
            background-color: #f8f9fa;
        }
        
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        
        /* Ensure all text is visible */
        p, h1, h2, h3, h4, h5, h6, span, div {
            color: #1f1f1f;
        }
        
        /* Make markdown text visible */
        .element-container {
            color: #1f1f1f;
        }
    </style>
""", unsafe_allow_html=True)

# Async MCP tool wrappers
def add_tool(input_str: str) -> str:
    async def _add():
        try:
            a, b = map(int, input_str.strip().split())
        except Exception:
            raise ValueError("Input must be two numbers separated by a space, e.g., '10 20'.")
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/add", json={"a": a, "b": b})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_add())

def reverse_string_tool(s: str) -> str:
    async def _reverse():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/reverse_string", json={"s": s})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_reverse())

def word_count_tool(s: str) -> str:
    async def _count():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/word_count", json={"s": s})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_count())

def wikipedia_summary_tool(query: str) -> str:
    async def _wiki():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/wikipedia_summary", json={"query": query})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_wiki())

def web_search_tool(query: str) -> str:
    async def _web():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/web_search", json={"query": query})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_web())

def python_exec_tool(code: str) -> str:
    async def _pyexec():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/python_exec", json={"code": code})
            print("PYTHON EXEC RESPONSE:", response.text)
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_pyexec())

def greet_tool(name: str) -> str:
    async def _greet():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/greet", json={"name": name})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_greet())

def tool1_tool(question: str) -> str:
    async def _tool1():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/tool1", json={"question": question})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_tool1())

def tool2_tool(question: str) -> str:
    async def _tool2():
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/tools/tool2", json={"question": question})
            return response.json().get("answer", "No answer returned.")
    return asyncio.run(_tool2())

# Define LangChain tools
tools = [
    Tool(
        name="Add",
        func=add_tool,
        description="Add two numbers. Input must be two numbers separated by a space, e.g., '10 20'."
    ),
    Tool(
        name="ReverseString",
        func=reverse_string_tool,
        description="Reverse a string. Input should be the string to reverse."
    ),
    Tool(
        name="WordCount",
        func=word_count_tool,
        description="Count the number of words in a string. Input should be the string."
    ),
    Tool(
        name="WikipediaSummary",
        func=wikipedia_summary_tool,
        description="Get a summary for a topic from Wikipedia. Input should be the topic."
    ),
    Tool(
        name="WebSearch",
        func=web_search_tool,
        description="Search the web for up-to-date information. Input should be the search query."
    ),
    Tool(
        name="PythonExec",
        func=python_exec_tool,
        description="Execute a Python code snippet and return the output. Input should be a valid Python expression, e.g., 'sum([1,2,3])' or 'max(5, 10)'. Only safe built-ins are allowed."
    ),
    Tool(
        name="Greet",
        func=greet_tool,
        description="Greet a person by name. Input should be the name."
    ),
    Tool(
        name="Tool1",
        func=tool1_tool,
        description="Tool1: Input should be a question."
    ),
    Tool(
        name="Tool2",
        func=tool2_tool,
        description="Tool2: Input should be a question."
    ),
]

# Custom system prompt
def get_llm():
    return ChatOpenAI(
        temperature=0,
        model=config.OPENAI_MODEL,
        openai_api_key=config.OPENAI_API_KEY
    )

# Add conversation memory
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
    )

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header with explicit text color
st.markdown("""
<div class="header">
    <h1 style="color: #1f1f1f;">🤖 MCP Chat Agent</h1>
    <p style="color: #666;">Powered by LangChain + FastAPI + Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with available tools
with st.sidebar:
    st.markdown("### 🛠️ Available Tools")
    for tool in tools:
        with st.expander(f"📍 {tool.name}"):
            st.write(tool.description)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        if "memory" in st.session_state:
            del st.session_state.memory
        st.rerun()

# Chat messages display
for msg in st.session_state.chat_history:
    message_class = "user-message" if msg["role"] == "user" else "agent-message"
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="timestamp">{avatar} {msg["role"].title()} • {msg.get("timestamp", "")}</div>
        <div class="content">{msg["content"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display agent reasoning if available
    if msg.get("chain_of_thought"):
        with st.expander("🔍 View Agent's Chain of Thought"):
            for step in msg["chain_of_thought"]:
                if "thought" in step:
                    st.markdown("""
                    <div class="reasoning-box">
                        <strong>🤔 Thought:</strong><br/>
                        {}</div>
                    """.format(step["thought"]), unsafe_allow_html=True)
                if "action" in step:
                    st.markdown("""
                    <div class="tool-box">
                        <strong>🛠️ Action:</strong> {}<br/>
                        <strong>Input:</strong> {}</div>
                    """.format(step["action"], step["action_input"]), unsafe_allow_html=True)
                if "observation" in step:
                    st.markdown("""
                    <div class="answer-box">
                        <strong>👁️ Observation:</strong><br/>
                        {}</div>
                    """.format(step["observation"]), unsafe_allow_html=True)

# Input area
st.markdown("### 💭 Ask me anything!")
question = st.text_input(
    "",
    placeholder="Try: 'Add 5 and 7' or 'Search the web for latest AI news'",
    key="input"
)

col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    if st.button("🚀 Ask", use_container_width=True) and question.strip():
        agent = get_agent()
        with st.spinner("🤔 Thinking..."):
            try:
                # Execute agent and get result with intermediate steps
                result = agent.invoke({"input": question})
                
                # Extract chain of thought from intermediate steps
                chain_of_thought = []
                if "intermediate_steps" in result:
                    for action, observation in result["intermediate_steps"]:
                        chain_of_thought.append({
                            "thought": action.log,
                            "action": action.tool,
                            "action_input": action.tool_input,
                            "observation": observation
                        })
                
                # Format the final answer
                answer = result["output"] if isinstance(result, dict) and "output" in result else result
                now = datetime.datetime.now().strftime("%H:%M:%S")
                
                # Add messages to chat history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question,
                    "timestamp": now
                })
                st.session_state.chat_history.append({
                    "role": "agent",
                    "content": markdown.markdown(answer),
                    "timestamp": now,
                    "chain_of_thought": chain_of_thought
                })
                st.rerun()
            except Exception as e:
                st.error(f"🚨 Agent error: {str(e)}") 