import streamlit as st
import os
from dotenv import load_dotenv

# Standard LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents.agent import AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Ubuntu AI Agent", layout="centered")
st.title("🐧 Gemini Search Agent")

# Corrected model to 1.5-flash (standard stable version)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define the Tool
tavily_search = TavilySearchAPIWrapper(tavily_api_key=os.getenv("TAVILY_API_KEY"))
search_tool = TavilySearchResults(api_wrapper=tavily_search, max_results=3)

# Define the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that uses tools for real-time info."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# Create Agent and Executor
agent = create_tool_calling_agent(llm, [search_tool], prompt)
executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# User Input
if user_input := st.chat_input("Ask a question..."):
    st.chat_message("user").markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            # Convert session history to list of tuples for the agent
            history = [(m["role"], m["content"]) for m in st.session_state.messages]
            
            response = executor.invoke({
                "input": user_input,
                "chat_history": history
            })
            st.markdown(response["output"])
            
    # Save to history
    st.session_state.messages.append({"role": "human", "content": user_input})
    st.session_state.messages.append({"role": "ai", "content": response["output"]})