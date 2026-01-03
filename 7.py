from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
     api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0", # Use a stable version for best results
    temperature=0.3
)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])
chain = prompt | llm
# Use a variable so you can check what was typed
user_input = input("Enter message: ")

if user_input.lower() == "hai":
    print("hello")

elif user_input.lower() == "hello":
    print("This is my special message for you!")

else:
   
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_input,
    )
    response = chain.invoke({"question": user_input})
    print(response.text)