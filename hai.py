def chatbot_response(user_input):
    # Rule-based intercept
    if user_input.lower().strip() == "hello":
        return "hai"
    
    # Logic for anything else
    else:
        return "I am a simple bot. Try typing 'hello'!"

# This part makes it interactive
print("--- Chatbot Active (Type 'exit' to stop) ---")

while True:
    # This line waits for you to type something and press Enter
    user_text = input("You: ")

    # Check if you want to stop the program
    if user_text.lower() in ["exit", "quit", "stop"]:
        print("Bot: Goodbye!")
        break

    # Get the response from our function
    response = chatbot_response(user_text)
    
    # Print the result
    print(f"Bot: {response}")