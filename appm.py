import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents.agent import AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# --- Page Config & Styling ---
st.set_page_config(page_title="AI Shopping Consultant", page_icon="🛒")
st.title("🛒 AI Shopping Assistant")
st.markdown("---")

# --- Initialize LLM and Tools ---
# Note: Use gemini-1.5-flash as gemini-2.5 is not released.
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

tavily_search = TavilySearchAPIWrapper(tavily_api_key=os.getenv("TAVILY_API_KEY"))
search_tool = TavilySearchResults(api_wrapper=tavily_search, max_results=3)

# --- The Optimized Prompt ---
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional Shopping Consultant. 
    Your goal is to find the perfect product by following a natural conversation.

    **CONVERSATIONAL RULES:**
    1. **One Step at a Time**: Ask ONLY ONE question per message.
    2. **Readability**: Use **bolding** for important terms and bullet points for lists.
    3. **The Workflow**:
       - Step 1: Acknowledge the product and ask for the **Primary Use Case**.
       - Step 2: Ask for a specific **Technical Requirement** (e.g., size, weight, or power).
       - Step 3: Ask for the **Budget Range**.
       - Step 4: Use tools to find and present 3 specific recommendations.

    Check `chat_history` carefully. If a detail was already provided, skip to the next step immediately."""),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# Create Agent
agent = create_tool_calling_agent(llm, [search_tool], prompt)
executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Chat History ---
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# --- Chat Input & Execution ---
if user_input := st.chat_input("I want to buy a laptop..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = executor.invoke({
                "input": user_input,
                "chat_history": st.session_state.chat_history
            })
            
            agent_response = response["output"]
            st.markdown(agent_response)

    # Append to history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=agent_response))

# --- Sidebar Controls ---
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()