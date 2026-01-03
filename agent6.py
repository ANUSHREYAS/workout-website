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
    model="ggemini-2.5-flash", # Changed to 1.5 as 2.5 is not a standard release name yet
    google_api_key="AIzaSyAyiN0VNjVpkWchEMiE1tPeHFmqZ8dmkso" 
)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional Shopping Consultant. Your goal is to find the perfect product for the user by following a strict sequential conversation.

    **Readability Rules:**
    1. **One Question at a Time**: Never ask multiple questions in one message. Wait for the user to answer before moving to the next requirement.
    2. **Clear Formatting**: Use bold text for key terms and keep your sentences short.
    3. **The Flow**:
        - **Step 1**: Acknowledge the product and ask about the **Primary Use Case** (e.g., Gaming, Office, or Creative work).
        - **Step 2**: Based on the use case, ask for the most important **Technical Spec** (e.g., "Do you need a large screen or something portable?").
        - **Step 3**: Ask for the **Budget Range**.
        - **Step 4**: Use the search tool to find 3 options.
        - **Step 5**: Present options in a clear, bulleted list.

    Always check `chat_history` to see which step you are on. If the user has already provided a detail, move immediately to the next step."""),
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

print("--- 🛒 AI Shopping Assistant Started (Type 'exit' to stop) ---")

while True:
    # Use a clear separator for user input
    user_input = input("\n[YOU]: ")
    
    if user_input.lower() in ['exit', 'quit']:
        print("\n[SYSTEM]: Session ended. Happy shopping!")
        break
    
    # Execute the agent
    result = executor.invoke({
        "input": user_input, 
        "chat_history": chat_history
    })
    
    agent_response = result["output"]
    
    # Print the agent response with extra spacing for readability
    print("-" * 30)
    print(f"[AGENT]: {agent_response}")
    print("-" * 30)
    
    # Store history as formal message objects
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=agent_response))