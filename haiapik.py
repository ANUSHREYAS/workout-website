import google.generativeai as genai

# 1. Setup your Gemini API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# 2. Initialize the model (Gemini 1.5 Flash is fast and free)
model = genai.GenerativeModel('gemini-1.5-flash')

def chatbot_response(user_input):
    # --- Rule 1: The "Hello" Intercept ---
    if user_input.lower().strip() == "hello":
        return "hai"
    
    # --- Rule 2: Actual Gemini LLM Logic ---
    try:
        # Sends the user input to Gemini's brain
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# 3. Interactive Loop
print("--- Gemini Chatbot Active (Type 'exit' to stop) ---")

while True:
    user_text = input("You: ")

    if user_text.lower() in ["exit", "quit", "stop"]:
        print("Bot: Goodbye!")
        break

    # Get the response (will be 'hai' for 'hello', and AI for others)
    response = chatbot_response(user_text)
    
    print(f"Bot: {response}")