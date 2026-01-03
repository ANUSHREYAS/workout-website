from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv
import os
load_dotenv()
tavily_api_key = "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"
tavily_search = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
Search_tool = TavilySearchResults(api_wrapper=tavily_search,max_result=3)
result=Search_tool.invoke("What is the capital of India?")
print(result)