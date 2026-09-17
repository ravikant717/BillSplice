from app.db.database import settings
from google import genai

api_key = settings.GEMINI_API_KEY.strip()

print("Key exists:", bool(api_key))
print("Key length:", len(api_key))
print("Key starts with:", api_key[:5])

client = genai.Client(
    api_key=api_key
)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say hello in one word."
)

print(response.text)