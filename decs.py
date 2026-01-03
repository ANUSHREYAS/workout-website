from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents.agent import AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Tool (optional – for checking device prices, etc.)
tavily_search = TavilySearchAPIWrapper(
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)
search_tool = TavilySearchResults(api_wrapper=tavily_search, max_result=3)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a Smart Home Decision Maker.
Your job is to analyze user parameters and decide:
1. Is a smart home possible? (YES / NO / PARTIALLY)
2. Why?
3. What improvements are needed?
Be practical and realistic."""),
    ("human", "{input}")
])

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

# -------- SMART HOME PARAMETERS --------
smart_home_input = {
    "budget_usd": 5000,
    "house_size_sqft": 1200,
    "internet_quality": "good",     # poor / average / good
    "power_backup": True,           # inverter or UPS
    "existing_wiring": "modern",    # old / average / modern
    "number_of_rooms": 5,
    "security_priority": "high",    # low / medium / high
    "automation_level": "medium",   # basic / medium / advanced
    "voice_assistant": True,        # Alexa / Google
    "maintenance_skill": "low"      # low / medium / high
}

# Convert parameters to natural language
user_question = f"""
I want to build a smart home. Please analyze these parameters:

Budget: {smart_home_input['budget_usd']} USD
House size: {smart_home_input['house_size_sqft']} sqft
Rooms: {smart_home_input['number_of_rooms']}
Internet quality: {smart_home_input['internet_quality']}
Power backup available: {smart_home_input['power_backup']}
Existing wiring: {smart_home_input['existing_wiring']}
Security priority: {smart_home_input['security_priority']}
Automation level: {smart_home_input['automation_level']}
Voice assistant needed: {smart_home_input['voice_assistant']}
Maintenance skill: {smart_home_input['maintenance_skill']}

Tell me clearly if it is possible or not.
"""

# Run agent
result = executor.invoke({"input": user_question})

print("\nSMART HOME DECISION:\n")
print(result["output"])
