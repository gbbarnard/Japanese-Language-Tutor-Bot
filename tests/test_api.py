import os
import cohere
from dotenv import load_dotenv

# 1. Load .env file
load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise RuntimeError("COHERE_API_KEY is not set in .env")

print("Loaded key OK")

# 2. Use the *v2* client, NOT Client
co = cohere.ClientV2(api_key=api_key)

# 3. Call the v2 Chat endpoint
response = co.chat(
    model="command-r-plus-08-2024",   # or another Command-R model
    messages=[
        {"role": "user", "content": "こんにちは！短く自己紹介して。"},
    ],
    max_tokens=120,
)

# 4. v2 Chat returns a `message` object with a `content` list
text = response.message.content[0].text
print("Model output:", text)