from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader # uv add langchain_community , pypdf  --> it is basically a pdf loader
from langchain_text_splitters import RecursiveCharacterTextSplitter # $ uv add langchain-text-splitters
from langchain_openai import OpenAIEmbeddings # $ uv add langchain-openai
from langchain_qdrant import QdrantVectorStore # $ uv add langchain-qdrant, docker is prerequisite

load_dotenv()

#whatever my current location we have + nodejs.pdf file here
pdf_path = Path(__file__).parent / "nodejs.pdf"

# Loading the pdf file
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()  # Read PDF File
print(docs[0])
print(f"Total Pages in PDF: {len(docs)}")

# Chunking/ Splitting the documents

# Here we are only providing chunking configurations to langchain splitters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
# Actual chunking happens here 
split_docs = text_splitter.split_documents(documents=docs)

# Vector Embeddings
# Langchain openai embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Using [embedding_model] create embeddings of [split_docs] and store in DB

# first run docker compose up -d qdrant
# then go to http://localhost:6333 and create a collection named "learning_vectors"
# or use the dashboard link
# http://localhost:6333/dashboard#/welcome
# http://localhost:6333
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    # url="http://localhost:6333",
    url="http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("Indexing of Documents Done...")