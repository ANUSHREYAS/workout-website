from google import genai
from google.genai import types # Add this import for tools

client = genai.Client(api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0")

user_input = input("Enter message: ")

if user_input.lower() == "hai":
    print("hello")

elif user_input.lower() == "hello":
    print("This is my special message for you!")

else:
    # This configuration tells Gemini to use Google Search
    search_tool = types.Tool(
        google_search = types.GoogleSearch()
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_input,
        config=types.GenerateContentConfig(
            tools=[search_tool]
        )
    )
    print(response.text)