'''from langchain_google_genai import ChatGoogleGenerative
from langchain.prompts import ChatPromptTemplate


Llm=ChatGoogleGenerativeAI{
    model="gemini-3-flash-preview"
    temperature=0.3
}
client = genai.Client(api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0")
prompt=ChatPromptTemplate.from_message([
    ("system","you are a helpful assistant."),
    ("human","{question}")

])
chain=prompt|Llm
response=chain.invoke(

)'''