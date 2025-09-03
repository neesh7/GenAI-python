from typing_extensions import TypedDict
# To build edges we need to make below imports
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv

## Loading OpenAI API keys
load_dotenv()
client = OpenAI()
####################### State ######################################
# Here we are definig the state which will get updated after every node processing
class State(TypedDict):
    query:str
    llm_result:str | None

########################## Node 1 ###############################
# This function is our only Node required for objective
def chat_bot(state: State): # This is hint used in function defination to tell the expected type of input
    query = state['query']

    # OpenAI
    #llm call (Query)
    llm_response = client.chat.completions.create(
            model= 'gpt-4.1-mini',
            messages=[
                {"role":"user", "content":query}
          ]    )

    result = llm_response.choices[0].message.content
    state['llm_result'] = result
    return state

########################Designing graph/ Graph Construction ############################
# As of now we have an empty graph only
graph_builder = StateGraph(State)

# Build graph
# Added node into graph
graph_builder.add_node("chat_bot", chat_bot)

# Logic
# Added edges into graph which will basically tell the flow of code
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

# Add
# here we are finaly making our graph after compiling
graph = graph_builder.compile()



def main():
    user_inp = input("Please enter your query: ")

    # Graph Invocation
    _state = { 
        "query": user_inp,
        "llm_result":None
    }
    graph_result = graph.invoke(_state)
    print("graph result :", graph_result)

main()