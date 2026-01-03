from langchain_core.prompts import ChatPromptTemplate

# Create a chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "Explain {topic} in simple terms."),
    ]
)

# Fill the prompt with a value
formatted_prompt = prompt.format_messages(topic="LangChain")

# Print the result
for message in formatted_prompt:
    print(f"{message.type}: {message.content}")

