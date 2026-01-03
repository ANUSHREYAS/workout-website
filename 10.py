from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Setup the Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # Updated to a stable model name
    google_api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0", 
    temperature=0.3
)

# 2. Setup the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

# 3. Create the Chain
chain = prompt | llm

user_input = input("Enter message: ")

if user_input.lower() == "hai":
    print("hello")

elif user_input.lower() == "hello":
    print("This is my special message for you!")

else:
    # 4. Invoke the chain correctly
    # Removed the 'client.models...' line as it was causing the crash
    response = chain.invoke({"question": user_input})
    
    # 5. Use .content instead of .text
    print(response.content)