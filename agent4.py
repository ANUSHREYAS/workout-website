''''''
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
    google_api_key="AIzaSyAyiN0VNjVpkWchEMiE1tPeHFmqZ8dmkso" 
)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional Shopping Assistant. Your goal is to guide the user to the best product (e.g., a laptop) through a natural, one-question-at-a-time conversation.

    Follow this protocol:
    1. **Initial Inquiry**: When the user mentions an item, acknowledge it and ask ONLY ONE question about their primary use case (e.g., "Is this for gaming, professional work, or casual use?").
    2. **Iterative Questions**: After each user response, acknowledge their input and ask the NEXT logical question (e.g., screen size, portability, or brand preference).
    3. **Budget Finalization**: Once the specs are clear, ask: "What is your maximum budget for this purchase?"
    4. **The Search**: ONLY after you have (a) Use case, (b) Key preferences, and (c) Budget, use the `tavily_search_results_json` tool to find 3 real-time matches from Google/the web.
    5. **Presentation**: Show the results with links and prices, then ask if they want to adjust any detail.

    Check `chat_history` to see which questions you have already asked so the conversation always moves forward."""),
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
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [] 

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
    
    # Run the agent
    result = executor.invoke({
        "input": user_input, 
        "chat_history": chat_history
    })
    
    agent_response = result["output"]
    print(f"\nAgent: {agent_response}\n")
    
    # Update history using the core message objects for better reliability
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=agent_response))