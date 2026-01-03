import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Gemini Web Agent", layout="centered")
st.title("🌐 AI Search Assistant")

# --- INITIALIZE AGENT (Cached for performance) ---
@st.cache_resource
def get_agent_executor():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key="AIzaSyACJOBOiAw-63Xjz75tvps5srtzWZKX0mw" 
    )
    
    tavily_api_key = "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"
    tavily_search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
    search_tool = TavilySearchResults(api_wrapper=tavily_search, max_results=3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that can use tools."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm=llm, tools=[search_tool], prompt=prompt)
    return AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

executor = get_agent_executor()

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_input := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Searching the web..."):
            response = executor.invoke({"input": user_input})
            answer = response["output"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})