import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents.agent import AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# UI config
st.set_page_config(page_title="AI Search Agent", layout="centered")
st.title("🔍 AI Tool-Calling Agent")
st.write("Ask anything — I’ll search the web when needed.")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can use tools."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# Tavily search tool
tavily_search = TavilySearchAPIWrapper(
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)
search_tool = TavilySearchResults(
    api_wrapper=tavily_search,
    max_result=3
)

# Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=[search_tool],
    prompt=prompt
)

executor = AgentExecutor(
    agent=agent,
    tools=[search_tool],
    verbose=True
)

# Session chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("💬 Enter your question:")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        response = executor.invoke({
            "input": user_input,
            "chat_history": st.session_state.chat_history
        })

        st.session_state.chat_history.append(("human", user_input))
        st.session_state.chat_history.append(("ai", response["output"]))

# Display chat
for role, message in st.session_state.chat_history:
    if role == "human":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Agent:** {message}")
