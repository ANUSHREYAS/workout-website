'''from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0",
    temperature=0.3
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant."),
    ("human", "{question}")
])


chain = prompt | llm


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
    print(response.content)'''