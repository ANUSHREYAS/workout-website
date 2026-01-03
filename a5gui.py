import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents.agent import AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.messages import HumanMessage, AIMessage
import os

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="AI Shopping Consultant", page_icon="🛒")
st.title("🛒 AI Shopping Assistant")
st.markdown("I help you find the perfect product through a tailored step-by-step process.")

# --- 2. INITIALIZE AGENT (Cached to avoid re-running on every click) ---
@st.cache_resource
def setup_agent():
    # Replace with your actual keys or use environment variables
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBsH0g9LETLCpSwwzdKKZ-OMdL4ynowHEs"
    os.environ["TAVILY_API_KEY"] = "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"

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") # Use standard release name
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional Shopping Consultant. Your goal is to find the perfect product... (your prompt logic)"""),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    
    search_wrapper = TavilySearchAPIWrapper()
    search_tool = TavilySearchResults(api_wrapper=search_wrapper, max_results=3)
    
    agent = create_tool_calling_agent(llm=llm, tools=[search_tool], prompt=prompt)
    return AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

executor = setup_agent()

# --- 3. SESSION STATE FOR CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 4. DISPLAY CHAT MESSAGES ---
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- 5. CHAT INPUT LOGIC ---
if user_input := st.chat_input("What are you looking to buy today?"):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting marketplace..."):
            response = executor.invoke({
                "input": user_input,
                "chat_history": st.session_state.chat_history
            })
            agent_response = response["output"]
            st.markdown(agent_response)
    
    # Update History
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=agent_response))