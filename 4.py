from google import genai

client = genai.Client(api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0")

# Use a variable so you can check what was typed
user_input = input("Enter message: ")

if user_input.lower() == "hai":
    print("hello")

elif user_input.lower() == "hello":
    print("This is my special message for you!")

else:
    # This line only runs if the input wasn't 'hai' or 'hello'
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_input,
    )
    print(response.text)