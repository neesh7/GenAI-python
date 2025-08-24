from langchain_openai import OpenAIEmbeddings # $ uv add langchain-openai
from langchain_qdrant import QdrantVectorStore # $ uv add langchain-qdrant, docker is prerequisite
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
clinet=OpenAI()


# Vector Embeddings
# Langchain openai embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
vector_db = QdrantVectorStore.from_existing_collection(

    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

query = input("> ")


# vector similarity search in db
# Now we can use the vector store to query the indexed documents

search_results = vector_db.similarity_search(
    query=query,
    k=5  # Number of results to return   
    )

print("Retrieving Documents...")
# print(search_results)
# print(f"Found {len(search_results)} results for query: {query}")
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who asnweres user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
"""
# print(SYSTEM_PROMPT)

# Sending User Query + Relevant Context to OpenAI Model
# Now we can use the OpenAI model to generate a response based on the context
response = clinet.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
)
print("Generating Response...")
# print(response.choices[0].message.content)
print(f"🤖: {response.choices[0].message.content}")