from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import requests, json
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import interrupt, Command
# flake8: noqa

load_dotenv()


###################### State  #################################
class State(TypedDict):
    messages: Annotated[list, add_messages]
    
########################## Define tools ###############################
tools = []

@tool()
def human_assistance(query: str):
    """ Request assistance from a human"""
    # when interrupt is called this saves the state in db and kills the graph
    human_response = interrupt({"query": query})
    # once the user/ admin provides the input the graph will be picked back from db and will be resumed
    return human_response["data"]

tools.append(human_assistance)
################# using langchains chat model function #############

llm = init_chat_model(model_provider='openai', model='gpt-4.1')
llm_with_tools = llm.bind_tools(tools)

####################  Creating Nodes  ###########################
def chatbot(state:State):
    # response = llm.invoke(state['messages'])
    response = llm_with_tools.invoke(state['messages'])
    return {"messages": [response]}

# tool node
tool_node = ToolNode(tools = tools)
################ graph construction ##########################
graph_builder = StateGraph(State)

## adding node
graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('tools', tool_node)


# definig edges
graph_builder.add_edge(START, 'chatbot')
graph_builder.add_conditional_edges('chatbot', tools_condition)
graph_builder.add_edge('tools', 'chatbot')
graph_builder.add_edge('chatbot', END)

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

def user_chat():
    # mongodb://<username>:<pass>@<host>:<port>
    DB_URL = "mongodb://admin:admin@mongodb:27017"
    config = {'configurable':{'thread_id': '20'}}
    while True:
        # To connect with mongodb
        with MongoDBSaver.from_conn_string(DB_URL) as mongo_checkpointer:
            graph_with_mongo = create_chat_graph(mongo_checkpointer)
            user_query = input('>:')
                # Invoke the graph / Graph Invocation
                # Graph state is normally transient whenever we invoke graph it's a fresh graph and doesn't hold any prior memory
                # to provide such features that our new graph have old context we use checkpointing or persistence
            state = State(messages= [{"role":"user", "content": user_query}])
            
            for event in graph_with_mongo.stream(state, config, stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()
            # print("graph result :", graph_result)
            if 'exit' in user_query.casefold():
                break



def admin_call():
        # mongodb://<username>:<pass>@<host>:<port>
    DB_URL = "mongodb://admin:admin@mongodb:27017"
    config = {'configurable':{'thread_id': '20'}}
    # To connect with mongodb
    with MongoDBSaver.from_conn_string(DB_URL) as mongo_checkpointer:
        graph_with_mongo = create_chat_graph(mongo_checkpointer)
        
        state = graph_with_mongo.get_state(config=config)
        last_message = state.values['messages'][-1]
        
        tool_calls = last_message.additional_kwargs.get("tool_calls",[])
        user_query = None

        for call in tool_calls:
            if call.get("function", {}).get("name") == "human_assistance":
                args = call["function"].get("arguments", "{}")
                try:
                    args_dict = json.loads(args)
                    user_query = args_dict.get("query")
                except json.JSONDecodeError:
                    print("Failed to decode function arguments.")

        print("User Has a Query", user_query)
        solution = input("> ")

        resume_command = Command(resume={"data": solution})

        for event in graph_with_mongo.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()
    pass






user_chat()
# admin_call()