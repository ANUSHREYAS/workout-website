'''import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# 1. Initialize the LLM
# LangChain uses ChatGoogleGenerativeAI instead of genai.Client
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", # Use a stable model name
    google_api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0",
    temperature=0.3
)

# 2. Create the Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant."),
    ("human", "{question}")
])

# 3. Create the Chain (LCEL - LangChain Expression Language)
chain = prompt | llm

# 4. Your custom logic
user_input = input("Enter message: ")

if user_input.lower() == "hai":
    print("hello")
elif user_input.lower() == "hello":
    print("This is my special message for you!")
else:
    # 5. Invoke the chain
    # We pass the input as a dictionary matching the {question} placeholder
    response = chain.invoke({"question": user_input})
    
    # LangChain returns a message object, so we print the .content
    print(response.content)'''