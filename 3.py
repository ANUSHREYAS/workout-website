from google import genai

client = genai.Client(api_key="AIzaSyBZs_4l1s_Q9WjOUxLzF7ztMhAhtK7ESf0")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)