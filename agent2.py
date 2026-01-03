
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_classic.agents.agent import AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Changed to 1.5 as 2.5 is not a standard release name yet
    google_api_key="AIzaSyA8TIP07gzlBd2j4ICnR0-oCgMy9Wnjw20" 
)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional Shopping Assistant specialized in helping users find the perfect products, such as laptops.
    
    Follow this iterative process strictly:
    1. **Discovery Phase**: If the user mentions an item they want to buy, do NOT search immediately. Instead, ask 2-3 clarifying questions to understand their specific needs (e.g., Is it for gaming, work, or student use? What screen size do they prefer?).
    2. **Recommendation Phase**: Once you have their preferences, provide a few general recommendations based on your internal knowledge.
    3. **Budget Phase**: After giving initial suggestions, ask the user for their specific budget or any other critical feature they haven't mentioned yet.
    4. **Search Phase**: ONLY after you have the budget and specific features, use the `tavily_search_results_json` tool to find real-time, up-to-date products from the web that match all their criteria (specs + budget).
    5. **Finalization**: Present the best options found online with links/prices and ask if they need help with any other detail until they find the "correct" item.
    
    Always check the `chat_history` to see which stage of the process you are in so you don't repeat questions."""),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
tavily_api_key = "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"
tavily_search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
Search_tool = TavilySearchResults(api_wrapper=tavily_search,max_result=3)
agent=create_tool_calling_agent(llm=llm,tools=[Search_tool],prompt=prompt)
executor=AgentExecutor(
    agent=agent,
    tools=[Search_tool], 
    verbose=True
    )
