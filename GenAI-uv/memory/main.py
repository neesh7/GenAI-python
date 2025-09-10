from mem0 import Memory
import os, json
from dotenv import load_dotenv
from openai import OpenAI
# flake8: noqa
load_dotenv()
client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


config = {
    "version": "v1.1",
    # this configuration belongs to embedder
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    # this for chat llm
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4.1"}
        },
    # it needs a vector store to store the embeddings too 
    "vector_store": {        
        "provider": "qdrant",
        "config": {
            "host": "localhost", # pass the name what you provided in docker-compose
            # "host": "vector-db", # if running inside devcontainer then use the container name directly and if running locally use localhost instead
            "port": "6333"}
        },
    "graph_store": {        
        "provider": "neo4j",
        "config": {
            # "url": "bolt://neo4j:7687",
            "url": "bolt://localhost:7687", # localhost:7474/browser/preview/
            "username": "neo4j",
            "password": "reform-william-center-vibrate-press-5829"}
            }
}

# by here our memory setup is ready/ basically to implement memory we are using rag only
mem_client = Memory.from_config(config)


# chatting with openai model
def chat():
    while True:
        user_query = input("> ")

        # reading all memories
        # all_memories = mem_client.get_all(user_id= "Neesh") # this will retrieve all memories about user but chances we might get off the context

        # fetch relevant memories
        relevant_memories = mem_client.search(query=user_query, user_id="Neesh") # using this it will do vector similarity search and will provide only those  memories which are relavnt for the user
        
        memories = [f"ID: {mem.get("id")} Memory: {mem.get("memory")}" for mem in relevant_memories.get("results")]

        SYSTEM_PROMPT = f"""
            You are an memeory aware assistant which responds to user with context.
            You are given with past memories and facts about the user.
            
            Memory of the user:
            {json.dumps(memories)}
        """
        llm_reponse = client.chat.completions.create(
                model= "gpt-4.1",
                messages= [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query}]
        )
        print(llm_reponse.choices[0].message.content)
        # Now adding our conversation into memory
        mem_client.add([
                {"role": "user", "content": user_query},
                {"role": "AI", "content":llm_reponse.choices[0].message.content }
                ],
                    user_id="Neesh" # similar to thread id    
                        )


chat()