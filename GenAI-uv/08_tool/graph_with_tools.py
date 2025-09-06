from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
# flake8: noqa

load_dotenv()


############### Making tools ###################
@tool()  # by using this decorator it will become a tool of langchain.
def get_weather(city: str):
    """summary: This tools checks weather of the provided city
    Args:
        city (str): we will pass the city name for which we want to check the weather
    Returns:
        str : it will return the temperature in celcius for the asked city
    """
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"

@tool()
def add_two_num(x: int ,y : int):
    """This tool returns sum of 2 number"""
    return x + y 
################ Database auto update using ai #############
# let's assume todo as our database array
todo = [] 

# create
@tool()
def write_data(task: str):
    """Adds the input task to DB"""
    todo.append(task)
    return todo

# read
@tool()
def get_data():
    """read the db"""
    return todo

# update
@tool()
def update_data(old_task, new_task):
    """Updates the old task with new task basically kind of replacement"""
    for i in todo:
        todo[old_task] = new_task
    return todo


# delete
@tool()
def delete_data(task):
    """Removes the provided task in args from DB/todo array"""
    todo.remove(task)
    return todo
# as per langchain prepare a array for your external tools like below
tools = [get_weather, add_two_num]

tools += [write_data, get_data, update_data, delete_data]

##################### State ##########################
class State(TypedDict):
    messages: Annotated[list, add_messages]

################# using langchains chat model function #############

llm = init_chat_model(model_provider='openai', model='gpt-4.1')
llm_with_tools = llm.bind_tools(tools)


####################  Node  ###########################
def chat_bot(state:State):
    # response = llm.invoke(state['messages'])
    response = llm_with_tools.invoke(state['messages'])
    return {"messages": [response]}

########## Graph construction  #######################
tool_node = ToolNode(tools=tools)
builder = StateGraph(State)
# Adding nodes
builder.add_node("chatbot", chat_bot)
builder.add_node("tools", tool_node)
# Adding Edges
builder.add_edge(START, "chatbot")

builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

builder.add_edge("tools", "chatbot")

#### compile graph ########
graph = builder.compile()

def main():
    while True:
        user_query = input('>')
        
        # Graph Invocation
        state = { 
            "messages": [{"role":"user", "content": user_query}]
        }
        # use streaming 
        for event in graph.stream(state, stream_mode='values'):
            if 'messages' in event:
                event['messages'][-1].pretty_print()
        if 'exit' in user_query:
            break
    # graph_result = graph.invoke(state)
    # print("graph result :", graph_result)
    
main()