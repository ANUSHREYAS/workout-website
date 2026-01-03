import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Try these more specific imports if the general one fails
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
    from langchain.agents.agent import AgentExecutor

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
# --- UI CONFIGURATION ---
st.set_page_config(page_title="Gemini Web Agent", layout="centered")
st.title("🌐 AI Search Assistant")

# --- INITIALIZE AGENT ---
@st.cache_resource
def get_agent_executor():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key="AIzaSyACJOBOiAw-63Xjz75tvps5srtzWZKX0mw" 
    )
    
    tavily_api_key = "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"
    tavily_search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
    # Note: Use max_results (plural) for modern versions
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching the web..."):
            # Ensure we pass the dictionary with the 'input' key
            response = executor.invoke({"input": user_input})
            answer = response["output"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})