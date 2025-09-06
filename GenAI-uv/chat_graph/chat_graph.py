from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
# flake8: noqa

load_dotenv()
client = OpenAI()


########### State  #####################
class State(TypedDict):
    messages: Annotated[list, add_messages] # Annotated list are those type of list which appends by default the elements to list if passed


llm = init_chat_model(model_provider='openai', model='gpt-4.1')
############ Node   #############################
def chat_node(state: State):
    response = llm.invoke(state['messages'])
    return {"messages": [response]}

#### Graph Build

builder = StateGraph(State)

# node add
builder.add_node('chat_node',chat_node)

# add edges
builder.add_edge(START, 'chat_node')
builder.add_edge('chat_node', END)

graph = builder.compile()
def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer = builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer
    

def main():
    # mongodb://<username>:<pass>@<host>:<port>
    DB_URL = "mongodb://admin:admin@mongodb:27017"
    config = {'configurable':{'thread_id': '1'}}
    # To connect with mongodb
    with MongoDBSaver.from_conn_string(DB_URL) as mongo_checkpointer:
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)
        user_query = input('>:')
            # Invoke the graph / Graph Invocation
            # Graph state is normally transient whenever we invoke graph it's a fresh graph and doesn't hold any prior memory
            # to provide such features that our new graph have old context we use checkpointing or persistence
        _state = { 
            "messages": [{"role":"user", "content": user_query}]
        } 
        # graph_result = graph.invoke(_state)
        graph_result = graph_with_mongo.invoke(_state, config)
        print("graph result :", graph_result)

main()