from dotenv import load_dotenv # loads the api key from the .env file
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "dog chases cat"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print("Vector Embeddings", response)
print(len(response.data[0].embedding))