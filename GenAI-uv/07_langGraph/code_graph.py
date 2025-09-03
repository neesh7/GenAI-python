from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal

load_dotenv()
client = OpenAI()

######################using pydantic base model to obtain only boolean output from classify messege ##############
class ClassifyMessegeResponse(BaseModel):
    is_coding_question: bool


class codeAccuracyPercentage(BaseModel):
    accuracy_percentage: str
####################### State ######################################
# Here we are definig the state which will get updated after every node processing
class State(TypedDict):
    user_query:str
    llm_result:str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None
########################## Our Node  ###############################
# Node1: This Node is to decide the query type --> is it a coding question or not
def classify_messege(state:State):
    print("Node1️⃣ Classify query ")
    query = state['user_query']

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is
    related to coding question or not.
    Return the response in specified JSON boolean only.
    """
    # make llm call to classify the query
    response = client.beta.chat.completions.parse( # we need to use beta in chat completeion to pass response_format or recieve structured response
            model= 'gpt-4.1-nano',
            response_format=ClassifyMessegeResponse, # to have a structure output/ response
            messages=[
                {"role":"system", "content":SYSTEM_PROMPT},
                {"role":"user", "content":query}
          ]    )

    is_coding_question = response.choices[0].message.parsed.is_coding_question # our response will be in form of true and false only/ basically controlling the output
    state['is_coding_question'] = is_coding_question
    return state


# Node2: Routing Node --> depending upon the response of Node 1 we want to handle the routes differently
# we need to define routing function like this because langgarph needs to know prior nodes where it can be routed
def route_query(state:State) -> Literal["general_query", "coding_query"]:
    print("Node2️⃣ Route Query")
    is_coding = state['is_coding_question']
    if is_coding:
        return "coding_query"
    else:
        return "general_query"


# Node3: General query resolver
def general_query(state:State):
    print("Node3️⃣ general query")
    user_query = state['user_query']
    llm_response = client.chat.completions.create(
            model= 'gpt-4.1-mini',
            messages=[
                {"role":"user", "content":user_query}
          ]    )
    result = llm_response.choices[0].message.content
    state['llm_result'] = result
    return state

# Node4: Coding Query resolver
def coding_query(state:State):
    print("Node4️⃣ Coding query")
    user_query = state['user_query']
    SYSTEM_PROMPT = """
        You are a Coding Expert Agent
    """
    llm_response = client.chat.completions.create(
            model= 'gpt-4.1', # we can even use claude from anthrophic also here
            messages=[
                {"role":"user", "content":user_query}
          ]    )
    result = llm_response.choices[0].message.content
    state['llm_result'] = result
    return state

# Node5: validating the coding result
def coding_validate_query(state:State):
    print("Node5️⃣ coding_validate_query")
    user_query = state['user_query']
    llm_code = state['llm_result']

    SYSTEM_PROMPT = f"""
        You are a Coding Expert Agent having expertise in calculating accuracy of the code.
        Expected output: please return the accuracy percentage for the provided code.
        User Query: {user_query}
        Code: {llm_code}
    """
    llm_response = client.beta.chat.completions.parse(
            model= 'gpt-4.1',
            response_format=codeAccuracyPercentage,
            messages=[
                {"role":"system", "content":SYSTEM_PROMPT},
                {"role":"user", "content":user_query}
          ]    )
    accuracy_percentage = llm_response.choices[0].message.parsed.accuracy_percentage
    state['accuracy_percentage'] = accuracy_percentage
    return state
########################Designing graph ############################
# As of now we have an empty graph only
graph_builder = StateGraph(State)

# Added nodes into graph
graph_builder.add_node("classify_messege", classify_messege)
graph_builder.add_node("route_query", route_query)
graph_builder.add_node("general_query", general_query)
graph_builder.add_node("coding_query", coding_query)
graph_builder.add_node("coding_validate_query", coding_validate_query)

# Added edges into graph which will basically tell the flow of code
graph_builder.add_edge(START, "classify_messege")
graph_builder.add_conditional_edges("classify_messege", route_query)
graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", "coding_validate_query")
graph_builder.add_edge("coding_validate_query", END)

# here we are finaly making our graph after compiling
graph = graph_builder.compile()

graph_builder = StateGraph(State)


def main():
    user_inp = input("Please enter your query: ")

    # Invoke the graph
    _state = { 
        "user_query": user_inp,
        "accuracy_percentage": None,
        "is_coding_question": False,
        "llm_result":None
    }
    graph_result = graph.invoke(_state)
    print("graph result :", graph_result)

main()