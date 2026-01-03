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
    ("system", "You are a helpful assistant that can use tools."),
    MessagesPlaceholder("chat_history", optional=True),#to save chat history
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
user_input=input("enter the question:")
result=executor.invoke({"input": user_input})
print(result)