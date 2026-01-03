from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

# Directly passing the API key here
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Changed to 1.5 as 2.5 is not a standard release name yet
    google_api_key="AIzaSyACJOBOiAw-63Xjz75tvps5srtzWZKX0mw" 
)
prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}")
])

chain = prompt | llm

user_input = input("Enter the question: ")
response = chain.invoke({"question": user_input})
print("\n--- Response ---")
print(response.content)