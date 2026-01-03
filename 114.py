rom langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}")
])

chain = prompt | llm

user_input = input("Enter the question: ")
response = chain.invoke({"question": user_input})

print(response.content)
