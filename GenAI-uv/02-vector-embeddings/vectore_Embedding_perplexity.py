import os
import requests
from dotenv import load_dotenv

load_dotenv()

# PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_KEY = ""
text = "dog chases cat"

url = "https://api.perplexity.ai/v1/embeddings"  # Hypothetical endpoint

headers = {
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "input": text,
    "model": "pplx-embedding-001"  # Hypothetical model name
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    embedding = data["embedding"]
    print("Vector Embeddings:", embedding)
    print("Length:", len(embedding))
else:
    print("Error:", response.status_code, response.text)
