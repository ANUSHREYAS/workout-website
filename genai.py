
from google import genai

client = genai.Client(api_key="AIzaSyBDdZa-w1x5ks8cn3_UD9o5HDF8B_6rEpU")


response = client.models.generate_content(
    
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)