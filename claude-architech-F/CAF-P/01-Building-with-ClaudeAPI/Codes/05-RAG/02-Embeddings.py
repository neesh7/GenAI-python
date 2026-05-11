import voyageai
import dotenv
import re


dotenv.load_dotenv()
client = voyageai.Client()


#### Chunking
# Chunk by section- Structure Based Chunking
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)



# Embedding
def generate_embeddings(text, model="voyage-large-2", input_type="document"):
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]

# Load file
with open("./report.md", "r") as f:
    text = f.read()

# Call chunking function
chunks = chunk_by_section(text)
# [print(chunk + "\n----\n") for chunk in chunks]

# Call Embedding generation
emb = generate_embeddings(chunks[0])
print(emb)