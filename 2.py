from google import genai

# Use your API Key
my_api_key = "AIzaSyBDdZa-w1x5ks8cn3_UD9o5HDF8B_6rEpU"
client = genai.Client(api_key=my_api_key)

def chatbot():
    print("--- Chatbot is Live! (Type 'quit' to exit) ---")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        if user_input == "quit":
            break
            
        # This part works even without internet/API!
        if user_input == "hello":
            print("Chatbot: hai")
        else:
            # This part talks to Google
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=user_input
                )
                print(f"Chatbot: {response.text}")
            except Exception as e:
                # If you see "429", it means wait 30 seconds and try again
                print(f"\n[AI Error]: {e}")

if __name__ == "__main__":
    chatbot()