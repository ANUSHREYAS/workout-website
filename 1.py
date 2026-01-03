from google import genai  # This is the ONLY import you need for the AI

# 1. Your API Key
my_api_key = "AIzaSyBDdZa-w1x5ks8cn3_UD9o5HDF8B_6rEpU"

# 2. Setup the Client
client = genai.Client(api_key=my_api_key)

def chatbot():
    print("--- Bot Started! Type 'hello' or 'quit' ---")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        if user_input == "quit":
            break
            
        # Your custom rule
        if user_input == "hello":
            print("Chatbot: hai")
        else:
            # Using the stable 2.0 Flash model
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=user_input
                )
                print(f"Chatbot: {response.text}")
            except Exception as e:
                print(f"AI Error: {e}")

if __name__ == "__main__":
    chatbot()